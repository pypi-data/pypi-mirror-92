from collections import defaultdict

from devito.logger import info


__all__ = ['Executor']


class Executor(object):

    """
    Abstract container class for a single benchmark data point.
    """

    def setup(self, **kwargs):
        """
        Prepares a single benchmark invocation.
        """
        pass

    def teardown(self, **kwargs):
        """
        Cleans up a single benchmark invocation.
        """
        pass

    def postprocess(self, **kwargs):
        """
        Global post-processing method to collect meta-data.
        """
        pass

    def reset(self):
        """
        Reset the data dictionaries.
        """
        self.meta = {}
        self.timings = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

    def run(self, **kwargs):
        """
        This method needs to be overridden by the user.
        """
        raise NotImplementedError("No custom executor function specified")

    def register(self, value, event='execute', measure='time', rank=0):
        """
        Register a single timing value for a given event key.

        Parameters
        ----------
        event : str
            key for the measured event, ie. 'assembly' or 'solve'
        value : float
            measured value to store
        measure : str
            name of the value type, eg. 'time' or 'flops'
        """
        self.timings[rank][event][measure] += value

    def execute(self, warmups=1, repeats=3, **params):
        """
        Execute a single benchmark repeatedly, including
        setup, teardown and postprocessing methods.
        """
        info("Running %d repeats - parameters: %s" % (repeats,
             ', '.join(['%s: %s' % (k, v) for k, v in params.items()])))

        self.reset()
        for i in range(warmups):
            info("--- Warmup %d ---" % i)
            self.setup(**params)
            self.run(**params)
            self.teardown(**params)
            info("--- Warmup %d finished ---" % i)

        self.reset()
        for i in range(repeats):
            info("--- Run %d ---" % i)
            self.setup(**params)
            self.run(**params)
            self.teardown(**params)
            info("--- Run %d finished ---" % i)

        info("")

        # Average timings across repeats
        for rank in self.timings.keys():
            for event in self.timings[rank].keys():
                for measure in self.timings[rank][event].keys():
                    self.timings[rank][event][measure] /= repeats

        # Collect meta-information via post-processing methods
        self.postprocess(**params)
