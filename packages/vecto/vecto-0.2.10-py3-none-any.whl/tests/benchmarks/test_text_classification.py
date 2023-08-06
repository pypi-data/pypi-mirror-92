"""Tests for analogy benchmark."""

import contextlib
import unittest
import io
from os import path
from vecto.benchmarks.text_classification import Benchmark as Text_classification
from vecto.benchmarks.text_classification import load_model, predict, get_vectors
from vecto.benchmarks import visualize
from vecto.embeddings import load_from_dir
from vecto.data import Dataset
from tests.test_setup import run_module

path_text_classification_dataset = path.join('.', 'tests', 'data', 'benchmarks', 'text_classification')
path_emb = path.join('tests', 'data', 'embeddings', 'text', 'plain_with_file_header')

class Tests(unittest.TestCase):

    def test_api(self):
        embs = load_from_dir(path_emb)
        dataset = Dataset(path_text_classification_dataset)

        tc = Text_classification(model='cnn')
        result = tc.run(embs, dataset,
                        "/tmp/vecto/benchmarks/text_classification_model/")
        self.assertIsInstance(result[0], dict)
        print(result)

        tc = Text_classification(model='rnn')
        result = tc.run(embs, dataset,
                        "/tmp/vecto/benchmarks/text_classification_model/")
        self.assertIsInstance(result[0], dict)
        print(result)

        tc = Text_classification(model='bow')
        result = tc.run(embs, dataset,
                        "/tmp/vecto/benchmarks/text_classification_model/")
        self.assertIsInstance(result[0], dict)
        print(result)

        model = load_model("/tmp/vecto/benchmarks/text_classification_model/args.json",
                                               embs.matrix)
        print(predict(model, "I like this"))
        print(get_vectors(model, ["I like this", "I hate this"]))

    def test_cli(self):
        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            run_module("vecto",
                       "benchmark",
                       "text_classification",
                       path_emb,
                       path_text_classification_dataset,
                       "--model", "cnn",
                       "--path_out", "/tmp/vecto/benchmarks/")

        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            run_module("vecto",
                       "benchmark",
                       "text_classification",
                       path_emb,
                       path_text_classification_dataset,
                       "--model", "cnn",
                       "--path_out", "/tmp/vecto/benchmarks/")

        with self.assertRaises(FileNotFoundError):
            sio = io.StringIO()
            with contextlib.redirect_stdout(sio):
                run_module("vecto",
                           "benchmark",
                           "text_classification",
                           path_emb + "NONEXISTING",
                           path_text_classification_dataset,
                           "--path_out", "/tmp/vecto/benchmarks/")

        from matplotlib import pyplot as plt
        visualize.plot_accuracy("/tmp/vecto/benchmarks/text_classification", key_secondary="experiment_setup.dataset")
        plt.savefig("/tmp/vecto/benchmarks/text_classification.pdf", bbox_inches="tight")

