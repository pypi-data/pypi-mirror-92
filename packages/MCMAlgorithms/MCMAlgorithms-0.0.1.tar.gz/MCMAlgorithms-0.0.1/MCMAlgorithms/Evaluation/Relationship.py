import numpy as np
import scipy.optimize as optim
import copy


class GreyAnalysis:

    def __init__(self, rho=0.5, mode='average'):
        """
        The setting of gray analysis
        :param rho: recognition coefficient, with default as 0.5, positive float
        :param mode: the method of removing dimension, with default as 'average', string in ('first', 'average')
        """
        self.__rho = rho
        self.__mode = mode.lower() if mode.lower() in ('first', 'average') else 'average'

    def analyse(self, base, data):
        """
        Apply grey analysis
        :param base: base sequence, list of numbers, 1-D ndarray or 1-D torch tensor
        :param data: 2-D ndarray, sequences for relationship calculating, each column is a sequence, the length should be equal to base
        :return: 1-D ndarray, each element indicates the corresponding relationship between the sequence and the base sequence
        """
        # Initialization
        base = np.array(base).squeeze()
        data = np.array(data)
        assert len(base) == data.shape[0]
        standard = np.mean(data, 0) if self.__mode == 'average' else data[0, :]
        no_dimension_data = data / standard
        standard = np.mean(base) if self.__mode == 'average' else base[0]
        no_dimension_base = base / standard
        # Calculate the relationship
        delta = np.abs(no_dimension_base.reshape(-1, 1) - no_dimension_data)
        max_relationship = np.max(delta)
        min_relationship = np.min(delta)
        xis = (min_relationship + self.__rho * max_relationship) / (delta + self.__rho * max_relationship)
        relationship = np.mean(xis, 0)
        return relationship


class DataEnvelope:

    def analyse(self, inputs, outputs):
        """
        Apply DEA analysis
        :param inputs: input data, with each column as a kind of input and row as observation, 2-D ndarray or 2-D torch tensor
        :param outputs: output data, with each column as a kind of output and row as observation, 2-D ndarray or 2-D torch tensor
        :return: efficient of each observation
        """
        # Initialization
        inputs = np.array(inputs)
        outputs = np.array(outputs)
        object_num, inputs_num = inputs.shape
        outputs_num = outputs.shape[1]
        # Programming
        b = np.zeros((object_num, 1))
        A = np.hstack((-outputs, inputs))
        evaluation = np.zeros(object_num)
        for idx in range(object_num):
            c = np.hstack((outputs[idx, :], np.zeros((1, inputs_num)).squeeze()))
            aeq = np.hstack((np.zeros((1, outputs_num)).squeeze(), inputs[idx, :])).reshape(1, -1)
            beq = 1
            x = optim.linprog(-c, -A, b, aeq, beq, [(0, None)] * len(c))
            x = x.x
            evaluation[idx] = np.sum(x * c.squeeze())
        return evaluation


class TOPSIS:

    def __change(self, M, a, b, x):
        if x < a:
            return 1 - (a - x) / M
        elif x > b:
            return 1 - (x - b) / M
        else:
            return 1

    def analyse(self, data, attribute_type=None, attribute_weight=None):
        # Initialization
        data = copy.deepcopy(data)
        attribute_num = data.shape[1]
        if attribute_type is None:
            attribute_type = dict.fromkeys(range(attribute_num))
            for num in range(attribute_num):
                attribute_type[num] = (1,)
        attribute_weight = np.ones(attribute_num) if attribute_weight is None else attribute_weight
        # Change the attribute to type 1
        for idx in range(attribute_num):
            if attribute_type[idx][0] == 2:
                data[:, idx] = np.max(data[:, idx]) - data[:, idx]
            elif attribute_type[idx][0] == 3:
                best = attribute_type[idx][1]
                M = np.max(np.abs(data[:, idx] - best))
                data[:, idx] = 1 - np.abs(data[:, idx] - best) / M
            elif attribute_type[idx][0] == 4:
                (a, b) = attribute_type[idx][1]
                if a > b:
                    a, b = b, a
                if a == b:
                    best = a
                    M = np.max(np.abs(data[:, idx] - best))
                    data[:, idx] = 1 - np.abs(data[:, idx] - best) / M
                else:
                    M = np.max([a - np.min(data[:, idx]), np.max(data[:, idx]) - b])
                    data[:, idx] = np.array(list(map(lambda x: self.__change(M, a, b, x), data[:, idx])))
        # Standardization
        data = data / np.sqrt(np.sum(data ** 2, 0))
        # Calculate the score
        z_plus = np.max(data, 0)
        z_minus = np.min(data, 0)
        d_plus = np.sqrt(np.sum(attribute_weight * (z_plus - data) ** 2, 1))
        d_minus = np.sqrt(np.sum(attribute_weight * (z_minus - data) ** 2, 1))
        score = d_minus / (d_plus + d_minus)
        return score
