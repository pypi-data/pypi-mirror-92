# This script contain functions help quantization
# Author:
#     Albert Dongz
# History:
#     2020.7.16 First Release
# Dependencies:
#     PyTorch
# Attention:
#     1. Nothing

import json
from .operators import *
from .utils import *

from tensorboardX import SummaryWriter


class QNQ():
    def __init__(self,
                 model,
                 save_path="./checkpoints/test",
                 config_file=None,
                 ext_metrics=None,
                 steper=None):
        # init parameters
        self.model = model
        self.save_path = save_path
        self.config_file = config_file
        # ext_metrics return a float value for search
        self.ext_metrics = ext_metrics
        self.steper = steper

        # init abstract log path and logger
        self.logger, self.log_path = lognow(self.save_path)
        self.writer = SummaryWriter(log_dir=os.path.normpath(self.log_path +
                                                             '/' + 'tblogs'))

        # load custom config
        try:
            self.load_config()
        except IOError:
            if not os.path.exists(os.path.dirname(self.config_file)):
                os.makedirs(os.path.dirname(self.config_file))
            self.init_config()
            self.logger.warning("Detect no config, creating...")
            self.logger.warning("Please review config and re-run.")
            exit(1)

        # processing custom config
        # exec fuse
        if self.fuse_all:
            fuse_module(self.model)
        else:
            self.fuse(self.config_file)

        # initialize quantization
        self.quant_layer_list = []
        self.quant_names = []
        self.logger.info("Initialize quant layer.")
        self.logger.info("Initialize activation hook.")
        for name, module in self.model.named_modules():
            quant_layer = qnq_switch.get(type(module), None)
            if quant_layer:
                # initialize quant_layer
                quant_layer = quant_layer(name, module,
                                          self.qconfig[name]['bit_width'],
                                          self.logger, self.writer)
                quant_layer.weight_fl = self.qconfig[name]['weight_fl']
                quant_layer.activation_fl = self.qconfig[name]['activation_fl']
                quant_layer.concat_sign = self.qconfig[name]['concat_sign']
                quant_layer.scale_sign = self.qconfig[name]['scale_sign']
                # append quant_layer and name
                self.quant_layer_list.append(quant_layer)
                self.quant_names.append(name)
                quant_layer.register_get_activation_hook()
        self.transfer_bn2scale()
        self.logger.info("Here the quant layers.")
        self.logger.info(str(self.quant_names))

    @exe_time
    def search(self):
        #todo when 2 or more fl have same metrics, how to do?
        def quantize_params():
            self.logger.info("Quantizing params...")
            for layer in self.quant_layer_list:
                layer.quantize_params()

        def quantize_activation():
            self.logger.info("Quantizing activation...")
            for layer in self.quant_layer_list:
                layer.quantize_activation()

        def search_params(layer, metrics_tmp):
            # info log
            self.logger.info("      Now searching " + layer.name +
                             "'s weight_fl...")

            metrics = []
            for test_fl in range(layer.bit_width):
                # save forward time
                if test_fl == layer.weight_fl:
                    metrics.append(metrics_tmp)
                else:
                    layer.trim_params(debug_bw=layer.bit_width,
                                      debug_fl=test_fl)
                    metrics_test = self.ext_metrics()
                    metrics.append(metrics_test)
                    # info log
                    self.logger.info("      weight_fl: " + str(test_fl) +
                                     ", metrics: " + str(metrics_test))

            # get maximum metrics' index
            layer.weight_fl = metrics.index(max(metrics))

            # info log
            self.logger.info("      " + layer.name + "'s weight_fl=" +
                             str(layer.weight_fl) + ", metrics=" +
                             str(max(metrics)))

            # maintain best weight_fl
            layer.trim_params(debug_bw=layer.bit_width,
                              debug_fl=layer.weight_fl)

            return max(metrics)

        def search_activation(layer, metrics_tmp):
            # info log
            self.logger.info("      Now searching " + layer.name +
                             "'s activation_fl...")

            metrics = []
            for test_fl in range(layer.bit_width):
                if test_fl == layer.activation_fl:
                    metrics.append(metrics_tmp)
                else:
                    layer.trim_activation(debug_bw=layer.bit_width,
                                          debug_fl=test_fl)
                    metrics_test = self.ext_metrics()
                    metrics.append(metrics_test)
                    # info log
                    self.logger.info("      activation_fl: " + str(test_fl) +
                                     ", metrics: " + str(metrics_test))
            # get maximum metrics' index
            layer.activation_fl = metrics.index(max(metrics))

            # info log
            self.logger.info("      " + layer.name + "'s activation_fl=" +
                             str(layer.activation_fl) + ", metrics=" +
                             str(max(metrics)))

            # maintain best activation_fl
            layer.trim_activation(debug_bw=layer.bit_width,
                                  debug_fl=layer.activation_fl)

            return max(metrics)

        def search_concat(layers):
            metrics = []
            # todo test all bit_width be same
            for test_fl in range(layers[0].bit_width):
                for layer in layers:
                    layer.trim_activation(debug_bw=layer.bit_width,
                                          debug_fl=test_fl)
                metrics_test = self.ext_metrics()
                metrics.append(metrics_test)
                # info log
                self.logger.info("      activation_fl: " + str(test_fl) +
                                 ", metrics: " + str(metrics_test))
            # get maximum metrics' index
            for layer in layers:
                layer.activation_fl = metrics.index(max(metrics))

            # maintain best activation_fl
            for layer in layers:
                layer.trim_activation(debug_bw=layer.bit_width,
                                      debug_fl=layer.activation_fl)

            return max(metrics), metrics.index(max(metrics))

        def do_quantize_params():
            # quantize params
            quantize_params()
            # test quantized metrics
            self.logger.info("  Testing quantized params metrics...")
            for layer in self.quant_layer_list:
                layer.trim_params()
            metrics_params = self.ext_metrics()
            self.logger.info("    Quantized params metrics:" +
                             str(metrics_params))

            return metrics_params, metrics_params

        def do_search_params(metrics_mid, metrics_params):
            #? only search when metrics drop 2 * self.threshold
            if metrics_mid - metrics_params >= 2 * self.search_threshold:
                # recover un-trim before search
                for layer in self.quant_layer_list:
                    layer.recover_params()
                # search params
                for index, layer in enumerate(self.quant_layer_list):
                    #? only search when layer have params
                    if layer.weight_fl != -1:
                        self.logger.info("  " + str(index + 1) + "/" +
                                         str(len(self.quant_layer_list)) +
                                         " Checking " + layer.name +
                                         "'s weight_fl.")
                        layer.trim_params()
                        metrics_tmp = self.ext_metrics()
                        #? only search when metrics drop >= self.threshold
                        if metrics_mid - metrics_tmp >= self.search_threshold:
                            self.logger.info("    Need to search, weight_fl=" +
                                             str(layer.weight_fl) +
                                             ", metrics=" + str(metrics_tmp))
                            metrics_mid = search_params(layer, metrics_tmp)
                        else:
                            metrics_mid = metrics_tmp
                            self.logger.info(
                                "    No need to search, weight_fl=" +
                                str(layer.weight_fl) + ", metrics=" +
                                str(metrics_mid))
            else:
                metrics_mid = metrics_params
                self.logger.info("    No need to search params, metrics=" +
                                 str(metrics_params))
            return metrics_mid, metrics_mid

        def do_quantize_activation():
            # process activation
            assert self.steper, "Search need a steper."
            self.logger.info("Gathering activation...")
            self.steper()
            for layer in self.quant_layer_list:
                layer.steper_sign = True
            print(" ")

            # quantize activation
            quantize_activation()
            # test quantized metrics
            self.logger.info("  Testing quantized activation metrics...")
            for layer in self.quant_layer_list:
                layer.trim_activation()
            metrics_activation = self.ext_metrics()
            self.logger.info("    Quantized activation metrics: " +
                             str(metrics_activation))
            return metrics_activation, metrics_activation

        def do_search_activation(metrics_mid, metrics_activation):
            #? only search only search when metrics drop 2 * self.threshold
            if metrics_mid - metrics_activation >= 2 * self.search_threshold:
                #todo valide
                #? remove handler
                # recovery un-trim before search
                for layer in self.quant_layer_list:
                    if layer.hook_handler is not None:
                        layer.hook_handler.remove()
                # search activation
                for index, layer in enumerate(self.quant_layer_list):
                    #? only search when layer need trim activation
                    if layer.activation_fl != -1:
                        self.logger.info("  " + str(index + 1) + "/" +
                                         str(len(self.quant_layer_list)) +
                                         " Checking " + layer.name +
                                         "'s activation_fl.")
                        layer.trim_activation()
                        metrics_tmp = self.ext_metrics()
                        #? only search when metrics drop >= self.threshold
                        if abs(metrics_tmp -
                               metrics_mid) >= self.search_threshold:
                            self.logger.info(
                                "    Need to search, activation_fl=" +
                                str(layer.activation_fl) + ", metrics=" +
                                str(metrics_tmp))
                            metrics_mid = search_activation(layer, metrics_tmp)
                        else:
                            metrics_mid = metrics_tmp
                            self.logger.info(
                                "    No Need to search, activation_fl=" +
                                str(layer.activation_fl) + ", metrics=" +
                                str(metrics_tmp))
            else:
                metrics_mid = metrics_activation
                self.logger.info("    No need to search activation, metrics=" +
                                 str(metrics_activation))
            return metrics_mid

        def do_search_concat(metrics_mid):
            if self.concat_num == 0:
                self.logger.warning(
                    "Concat_num is zero, no need to do_search_concat.")
                return metrics_mid
            else:
                metrics_cat = 0
            self.logger.info("There are " + str(self.concat_num) +
                             " concat(s) need to process.")
            # make every group concat fl same
            for index in range(self.concat_num):
                concat_layer_list = []
                for layer in self.quant_layer_list:
                    if layer.concat_sign == index:
                        concat_layer_list.append(layer)
                concat_layer_name = [x.name for x in concat_layer_list]
                self.logger.info("  Now processing the " + str(index + 1) +
                                 "th concat.")
                self.logger.info("  They are " + str(concat_layer_name))
                # These layers' bit_width should be same.
                # todo test bitwidth
                metrics_cat, group_fl = search_concat(concat_layer_list)
                self.logger.info("  " + str(index + 1) +
                                 "th processing done, group_fl=" +
                                 str(group_fl) + ", metrics=" +
                                 str(metrics_cat))
            return metrics_cat

        assert self.ext_metrics, "Search need a metrics."
        self.logger.info("Configuration: ")
        self.logger.info("  Log_path: " + str(self.log_path))
        self.logger.info("  Fuse_all: " + str(self.fuse_all))
        self.logger.info("  Concat_num: " + str(self.concat_num))
        self.logger.info("  Quantize_params: " + str(self.quantize_params))
        self.logger.info("  Search_params: " + str(self.search_params))
        self.logger.info("  Quantize_activation: " +
                         str(self.quantize_activation))
        self.logger.info("  Search_activation: " + str(self.search_activation))
        self.logger.info("  Search_concat: " + str(self.search_concat))
        self.logger.info("  Threshold: " + str(self.search_threshold))
        self.logger.info("  Testing origin metrics...")
        metrics_final = metrics_origin = metrics_mid = self.ext_metrics()
        self.logger.info("    Initialization metrics: " + str(metrics_mid))

        if self.quantize_params:
            metrics_final, metrics_params = do_quantize_params()
        if self.search_params:
            assert self.quantize_params, "If you want to search params, you must set quantize_params=true in config file."
            metrics_final, metrics_mid = do_search_params(
                metrics_mid, metrics_params)

        if self.quantize_activation:
            assert self.quantize_activation, "If you want to search activation, you must set quantize_activation=true in config file."
            metrics_final, metrics_activation = do_quantize_activation()
        if self.search_activation:
            metrics_final = do_search_activation(metrics_mid,
                                                 metrics_activation)

        if self.search_concat:
            metrics_final = do_search_concat(metrics_final)

        if not [
                self.quantize_params, self.search_params,
                self.quantize_activation, self.search_activation,
                self.search_concat
        ]:
            self.logger.warning(
                "Oops, we have done nothing, pls check the program, and you shouldn't set all false."
            )
        else:
            self.save_config()

            self.logger.info("Quantization finished: ")
            self.logger.info("  Origin metrics: " + str(metrics_origin))
            self.logger.info("  After metrics: " + str(metrics_final))

    def step(self):
        for layer in self.quant_layer_list:
            layer.init_histograms()
        #? simulate processing bar
        print(".", end=" ")

    def save_config(self, config_file=None):
        # save quant_config
        # quantization config and quantization parameters
        qconfig = {}

        # config
        qconfig['config'] = {}
        qconfig['config']['fuse_all'] = self.fuse_all
        qconfig['config']['concat_num'] = self.concat_num
        qconfig['config']['quantize_params'] = self.quantize_params
        qconfig['config']['search_params'] = self.search_params
        qconfig['config']['quantize_activation'] = self.quantize_activation
        qconfig['config']['search_activation'] = self.search_activation
        qconfig['config']['search_concat'] = self.search_concat
        qconfig['config']['search_threshold'] = self.search_threshold
        qconfig['config']['notes'] = "'-1' means no operation."

        # layers' quantization parameters
        for layer in self.quant_layer_list:
            qconfig[layer.name] = {}
            qconfig[layer.name]['bit_width'] = int(layer.bit_width)
            qconfig[layer.name]['weight_fl'] = int(layer.weight_fl)
            qconfig[layer.name]['activation_fl'] = int(layer.activation_fl)
            qconfig[layer.name]['concat_sign'] = int(layer.concat_sign)
            qconfig[layer.name]['scale_sign'] = layer.scale_sign
            qconfig[layer.name]['layer_type'] = str(type(layer.module))[8:-2]

        if config_file:
            with open(config_file, 'w+') as file:
                json.dump(qconfig, file)
        else:
            with open(self.log_path + '/quant.json', 'w+') as file:
                json.dump(qconfig, file)

    def load_config(self):
        # open config
        with open(self.config_file, 'r') as f:
            self.qconfig = json.load(f)
        # load config
        self.fuse_all = self.qconfig['config']['fuse_all']
        self.concat_num = self.qconfig['config']['concat_num']
        self.quantize_params = self.qconfig['config']['quantize_params']
        self.search_params = self.qconfig['config']['search_params']
        self.quantize_activation = self.qconfig['config'][
            'quantize_activation']
        self.search_activation = self.qconfig['config']['search_activation']
        self.search_concat = self.qconfig['config']['search_concat']
        self.search_threshold = self.qconfig['config']['search_threshold']

    def init_config(self):
        #! 1 same with self.load_config
        #! 2 same with self.save_config
        #! 3 same with config.json
        #! 3 same with logger info
        # set default config
        self.fuse_all = True
        self.concat_num = 0
        self.quantize_params = True
        self.search_params = True
        self.quantize_activation = True
        self.search_activation = True
        self.search_concat = True
        self.search_threshold = 0.005  # 0.5%
        self.bit_width = 8
        # modify model arch because fuse_all default is True
        fuse_module(self.model)
        # initialization
        self.quant_layer_list = []
        for name, module in self.model.named_modules():
            quant_layer = qnq_switch.get(type(module), None)
            if quant_layer:
                quant_layer = quant_layer(name, module, self.bit_width,
                                          self.logger, self.writer)
                self.quant_layer_list.append(quant_layer)
        # save init_config file
        self.save_config(self.config_file)

    def fuse(self):
        pass

    def trim_activation(self, index=None, debug_bw=None, debug_fl=None):
        self.logger.info("Turn on eval mode.")
        if index != None:
            self.quant_layer_list[index].trim_activation(debug_bw, debug_fl)
        else:
            for layer in self.quant_layer_list:
                layer.trim_activation()

    def transfer_bn2scale(self):
        for layer in self.quant_layer_list:
            if layer.scale_sign:
                bn2scale(layer.module)