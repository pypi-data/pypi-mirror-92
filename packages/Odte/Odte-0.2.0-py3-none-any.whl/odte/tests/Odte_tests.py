# type: ignore
import unittest
import os
import random
import warnings
from sklearn.exceptions import ConvergenceWarning

from odte import Odte
from stree import Stree
from .utils import load_dataset


class Odte_test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self._random_state = 1
        super().__init__(*args, **kwargs)

    def test_max_samples_bogus(self):
        values = [0, 3000, 1.1, 0.0, "duck"]
        for max_samples in values:
            with self.assertRaises(ValueError):
                tclf = Odte(max_samples=max_samples)
                tclf.fit(*load_dataset(self._random_state))

    def test_get_bootstrap_nsamples(self):
        expected_values = [(1, 1), (1500, 1500), (0.1, 150)]
        for value, expected in expected_values:
            tclf = Odte(max_samples=value)
            computed = tclf._get_bootstrap_n_samples(1500)
            self.assertEqual(expected, computed)

    def test_initialize_max_feature(self):
        expected_values = [
            [6, 7, 8, 15],
            [3, 4, 5, 6, 10, 13],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            [6, 7, 8, 15],
            [6, 7, 8, 15],
            [6, 7, 8, 15],
        ]
        X, y = load_dataset(
            random_state=self._random_state, n_features=16, n_samples=10
        )
        for max_features in [4, 0.4, 1.0, None, "auto", "sqrt", "log2"]:
            tclf = Odte(
                random_state=self._random_state, max_features=max_features
            )
            tclf.fit(X, y)
            computed = tclf._get_random_subspace(X, y, tclf.max_features_)
            expected = expected_values.pop(0)
            self.assertListEqual(expected, list(computed))
            # print(f"{list(computed)},")

    def test_initialize_random(self):
        expected = [37, 235, 908]
        tclf = Odte(random_state=self._random_state)
        box = tclf._initialize_random()
        computed = box.randint(0, 1000, 3)
        self.assertListEqual(expected, computed.tolist())
        # test None
        tclf = Odte(random_state=None)
        box = tclf._initialize_random()
        computed = box.randint(101, 1000, 3)
        for value in computed.tolist():
            self.assertGreaterEqual(value, 101)
            self.assertLessEqual(value, 1000)

    def test_bogus_max_features(self):
        values = ["duck", -0.1, 0.0]
        for max_features in values:
            with self.assertRaises(ValueError):
                tclf = Odte(max_features=max_features)
                tclf.fit(*load_dataset(self._random_state))

    def test_bogus_n_estimator(self):
        values = [0, -1, 2]
        for n_estimators in values:
            with self.assertRaises(ValueError):
                tclf = Odte(n_estimators=n_estimators)
                tclf.fit(*load_dataset(self._random_state))

    def test_simple_predict(self):
        os.environ["PYTHONWARNINGS"] = "ignore"
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        X, y = [[1, 2], [5, 6], [9, 10], [16, 17]], [0, 1, 1, 2]
        expected = [0, 1, 1, 2]
        tclf = Odte(
            base_estimator=Stree(),
            random_state=self._random_state,
            n_estimators=10,
            n_jobs=-1,
        )
        tclf.set_params(
            **dict(
                base_estimator__kernel="rbf",
                base_estimator__random_state=self._random_state,
            )
        )
        computed = tclf.fit(X, y).predict(X)
        self.assertListEqual(expected, computed.tolist())

    def test_predict(self):
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        X, y = load_dataset(self._random_state)
        expected = y
        tclf = Odte(
            base_estimator=Stree(),
            random_state=self._random_state,
            max_features=1.0,
            max_samples=0.1,
        )
        tclf.set_params(
            **dict(
                base_estimator__kernel="linear",
            )
        )
        computed = tclf.fit(X, y).predict(X)
        self.assertListEqual(expected[:27].tolist(), computed[:27].tolist())

    def test_score(self):
        X, y = load_dataset(self._random_state)
        expected = 0.9526666666666667
        tclf = Odte(
            random_state=self._random_state,
            max_features=None,
            n_estimators=10,
        )
        computed = tclf.fit(X, y).score(X, y)
        self.assertAlmostEqual(expected, computed)

    def test_score_splitter_max_features(self):
        X, y = load_dataset(self._random_state, n_features=12, n_samples=150)
        results = [
            0.86,
            0.8933333333333333,
            0.9933333333333333,
            0.9933333333333333,
        ]
        random.seed(self._random_state)
        for max_features in ["auto", None]:
            for splitter in ["best", "random"]:
                tclf = Odte(
                    base_estimator=Stree(),
                    random_state=self._random_state,
                    max_features=max_features,
                    n_estimators=10,
                )
                tclf.set_params(
                    **dict(
                        base_estimator__splitter=splitter,
                        base_estimator__random_state=self._random_state,
                    )
                )
                expected = results.pop(0)
                computed = tclf.fit(X, y).score(X, y)
                # print(computed, splitter, max_features)
                self.assertAlmostEqual(expected, computed)

    def test_generate_subspaces(self):
        features = 250
        for max_features in range(2, features):
            num = len(Odte._generate_spaces(features, max_features))
            self.assertEqual(5, num)
        self.assertEqual(3, len(Odte._generate_spaces(3, 2)))
        self.assertEqual(4, len(Odte._generate_spaces(4, 3)))

    @staticmethod
    def test_is_a_sklearn_classifier():
        os.environ["PYTHONWARNINGS"] = "ignore"
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        from sklearn.utils.estimator_checks import check_estimator

        check_estimator(Odte())
