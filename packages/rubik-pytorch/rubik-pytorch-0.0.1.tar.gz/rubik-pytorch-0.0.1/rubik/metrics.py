import numpy as np
import torch
import sklearn.metrics as sk_metrics

class Metric():
    '''
    Metrics holds values during accumulation and reduce to stats in the \
        end, should be aware of memory issue when saving all scores with \
        with large datasets.
    '''
    
    def __init__(self):
        self.memory = []

    def reset_memory(self):
        self.memory = []

    def step_wrap(self, output_data):
        stats = self.step(output_data)
        self.memory.append(stats)

    def reduce_wrap(self, config):
        result = self.reduce(self.memory, config)
        self.reset_memory()
        return result

    def step(self, output_data):
        '''
        Store scores to avoid large RAM usage

        Args:
            output_data (tuple): Output from train function has form: \
                ``loss.item(), inputs, outputs, labels`` or form defined \ 
                by customized train function.

        Returns:
            list: an array of transformed stats for computation.
        '''
        raise NotImplementedError('Accumulation not implemented')

    def reduce(self, memory, config):
        '''
        Reduce arrays using the format in the accumulation phase

        Args:
            config (dict): Determine global progress, Metric is memoryless.
        '''
        raise NotImplementedError('Reduce not implemented')

class Accuracy(Metric):
    
    def step(self, output_data):
        loss, inputs, outputs, labels = output_data
        return outputs, labels

    def reduce(self, memory, config):
        outputs = [entry[0] for entry in memory]
        labels = [entry[1] for entry in memory]
        outputs = torch.argmax(torch.cat(outputs), dim = 1).cpu().numpy()
        labels = torch.cat(labels).cpu().numpy()
        score = sk_metrics.accuracy_score(labels, outputs)
        return score

class AUC(Metric):

    def step(self, output_data):
        loss, inputs, outputs, labels = output_data
        return outputs, labels

    def reduce(self, memory, config):
        outputs = [entry[0] for entry in memory]
        labels = [entry[1] for entry in memory]
        outputs = self.softmax(torch.cat(outputs).cpu().numpy())[:, 1]
        labels = torch.cat(labels).cpu().numpy()
        score = sk_metrics.roc_auc_score(labels, outputs)
        return score

    def softmax(self, x):
        return np.exp(x) / np.exp(x).sum(axis = 1, keepdims = True)

class F1(Metric):

    def step(self, output_data):
        loss, inputs, outputs, labels = output_data
        return outputs, labels

    def reduce(self, memory, config):
        outputs = [entry[0] for entry in memory]
        labels = [entry[1] for entry in memory]
        outputs = torch.argmax(torch.cat(outputs), dim = 1).cpu().numpy()
        labels = torch.cat(labels).cpu().numpy()
        print(sum(outputs))
        print(sum(labels))
        score = sk_metrics.f1_score(labels, outputs)
        return score
