import numpy as np
import torch

from medpy.metric.binary import (dc, jc, hd, asd, assd,
                                 precision, recall, ravd,
                                 sensitivity,
                                 specificity,
                                 true_positive_rate,
                                 true_negative_rate,
                                 positive_predictive_value)
from sklearn.metrics import (f1_score, precision_score, recall_score)


class Metrics():
    """Metrics class.

    Parameters
    ----------
    polyaxon_exp : poyaxon.tracking.Run
        polyaxon experiment.
    phase : type
        Description of parameter `phase`.
    metrics_strings : list
        list of metrics strings to evaluate
        during model training or evaluation.
    *args : list
        list of non keyworded arguments.
    **kwargs : type
        list of keyworded arguments.

    Attributes
    ----------
    metrics_strings : list
        list of metrics strings to evaluate
        during model training or evaluation.
    metric_funcs : list
        list of functions for every metric
        in metric_strings.
    metrics : dict
        map of evaluated metrics where
            key   : string from metrics_strings
            value : evaluated metrics.
    initialize_metrics : function
        method to initialise metrics map.

    """

    def __init__(self,
                 polyaxon_exp=None,
                 phase='',
                 metrics_strings=['prec'],
                 *args, **kwargs):
        super(Metrics, self).__init__(*args, **kwargs)
        self.polyaxon_exp = polyaxon_exp
        self.phase = phase
        self.metric_strings = metrics_strings
        self.metric_funcs = {}
        self.metrics = {}
        self.multilabel = False
        self.initialize_metrics()

    def initialize_metrics(self):
        """Initialise metrics map based on
            metrics in metric_strings.

        Following metric keys are allowed currently:

        dc(result, reference)
                                        Dice coefficient
        jc(result, reference)
                                        Jaccard coefficient
        hd(result, reference[, voxelspacing, …])
                                        Hausdorff Distance.
        asd(result, reference[, voxelspacing, …])
                                        Average surface distance metric.
        assd(result, reference[, voxelspacing, …])
                                        Average symmetric surface distance.
        prec(result, reference)
                                        Precison.
        recall(result, reference)
                                        Recall.
        sensi(result, reference)
                                        Sensitivity.
        speci(result, reference)
                                        Specificity.
        tpr(result, reference)
                                        True positive rate.
        tnr(result, reference)
                                        True negative rate.
        ppv(result, reference)
                                        Positive predictive value.
        ravd(result, reference)
                                        Relative absolute volume difference.

        """
        self.metrics['loss'] = []

        if 'dc' in self.metric_strings:
            self.metric_funcs['dc'] = dc
            self.metrics['dc'] = []

        if 'jc' in self.metric_strings:
            self.metric_funcs['jc'] = jc
            self.metrics['jc'] = []

        if 'hd' in self.metric_strings:
            self.metric_funcs['hd'] = hd
            self.metrics['hd'] = []

        if 'asd' in self.metric_strings:
            self.metric_funcs['asd'] = asd
            self.metrics['asd'] = []

        if 'assd' in self.metric_strings:
            self.metric_funcs['assd'] = assd
            self.metrics['assd'] = []

        if 'prec' in self.metric_strings:
            self.metric_funcs['prec'] = precision
            self.metrics['prec'] = []

        if 'recall' in self.metric_strings:
            self.metric_funcs['recall'] = recall
            self.metrics['recall'] = []

        if 'sensi' in self.metric_strings:
            self.metric_funcs['sensi'] = sensitivity
            self.metrics['sensi'] = []

        if 'speci' in self.metric_strings:
            self.metric_funcs['speci'] = specificity
            self.metrics['speci'] = []

        if 'tpr' in self.metric_strings:
            self.metric_funcs['tpr'] = true_positive_rate
            self.metrics['tpr'] = []

        if 'tnr' in self.metric_strings:
            self.metric_funcs['tnr'] = true_negative_rate
            self.metrics['tnr'] = []

        if 'ppv' in self.metric_strings:
            self.metric_funcs['ppv'] = positive_predictive_value
            self.metrics['ppv'] = []

        if 'ravd' in self.metric_strings:
            self.metric_funcs['ravd'] = ravd
            self.metrics['ravd'] = []

        if 'mc-prec' in self.metric_strings:
            self.metric_funcs['mc-prec'] = precision_score
            self.metrics['mc-prec'] = []

        if 'mc-recall' in self.metric_strings:
            self.metric_funcs['mc-recall'] = recall_score
            self.metrics['mc-recall'] = []

        if 'mc-f1-score' in self.metric_strings:
            self.metric_funcs['mc-f1-score'] = f1_score
            self.metrics['mc-f1-score'] = []

        if 'ml-prec' in self.metric_strings:
            self.multilabel = True
            self.metric_funcs['ml-prec'] = precision_score
            self.metrics['ml-prec'] = []

        if 'ml-recall' in self.metric_strings:
            self.multilabel = True
            self.metric_funcs['ml-recall'] = recall_score
            self.metrics['ml-recall'] = []

        if 'ml-f1-score' in self.metric_strings:
            self.multilabel = True
            self.metric_funcs['ml-f1-score'] = f1_score
            self.metrics['ml-f1-score'] = []

    def reset(self):
        """Reset metrics map.

        """
        for k in self.metrics.keys():
            self.metrics[k] = []

    def _transform_tensor(self, tensor):
        """Transform tensor into numpy array.

        Parameters
        ----------
        tensor : torch.Tensor
            tensor to transform.

        Returns
        -------
        numpy.ndarray
            numpy array transformed from tensor.

        """
        if isinstance(tensor, int):
            return tensor
        if isinstance(tensor, torch.Tensor):
            if tensor.is_cuda:
                return tensor.data.cpu().numpy()
            else:
                return tensor.data.numpy()
        if isinstance(tensor, np.ndarray):
            return tensor
        if isinstance(tensor, list):
            return np.asarray(tensor)

    def _argmax_or_thresholding(self, tensor):
        """Performs argmax or thresholding on input tensor.

        Parameters
        ----------
        tensor : torch.Tensor
            input tensor.

        Returns
        -------
        torch.Tensor
            final tensor after applying transforms.

        """
        if type(tensor) != torch.Tensor:
            raise TypeError("Input should be a torch tensor!")

        if len(tensor.size()) >= 4:
            if tensor.size(1) == 1:
                tensor = torch.squeeze(tensor, dim=1)
                tensor[tensor < 0.5] = 0
                tensor[tensor >= 0.5] = 1
            else:
                tensor = torch.argmax(tensor, dim=1)
        if len(tensor.size()) == 3:
            tensor[tensor < 0.5] = 0
            tensor[tensor >= 0.5] = 1
        if len(tensor.size()) == 2:
            if not self.multilabel:
                tensor = torch.argmax(tensor, dim=1)
            else:
                tensor[tensor < 0.5] = 0
                tensor[tensor >= 0.5] = 1

        return tensor

    def compute(self, predicted, target, loss):
        """Compute loss between target and predicted tensors.

        Parameters
        ----------
        predicted : torch.Tensor
            predicted/output tensor.
        target : torch.Tensor
            target tensor.
        loss : torch.Tensor
            loss tensor.

        """
        self.metrics['loss'].append(self._transform_tensor(loss))
        predicted = self._argmax_or_thresholding(predicted)

        for k in self.metric_funcs.keys():
            predicted = self._transform_tensor(predicted)
            target = self._transform_tensor(target)

            if 'mc' in k:
                self.metrics[k].append(self.metric_funcs[k](predicted.flatten(), target.flatten(),
                                                            average='micro'))
            elif 'ml' in k:
                self.metrics[k].append(self.metric_funcs[k](predicted, target,
                                                            average='samples'))
            else:
                self.metrics[k].append(self.metric_funcs[k](predicted, target))

    def crunch_it(self, epoch):
        """Crunch metrics to obtain mean_metrics map.

        Parameters
        ----------
        epoch : int
            model epoch.

        Returns
        -------
        dict
            mean_metrics map.

        """
        mean_metrics = {}
        for k in self.metrics.keys():
            if self.phase:
                out_key = self.phase + '_' + k
            else:
                out_key = k
            mean_metrics[out_key] = np.mean(self.metrics[k])

        if self.polyaxon_exp:
            self.polyaxon_exp.log_metrics(step=epoch, **mean_metrics)

        return mean_metrics
