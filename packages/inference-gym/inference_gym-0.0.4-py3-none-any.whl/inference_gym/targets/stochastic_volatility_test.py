# Lint as: python3
# Copyright 2020 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Tests for inference_gym.targets.stochastic_volatility."""

import tensorflow.compat.v2 as tf

from inference_gym.internal import test_util
from inference_gym.targets import stochastic_volatility


@test_util.multi_backend_test(globals(), 'targets.stochastic_volatility_test')
class StochasticVolatilityTest(test_util.InferenceGymTestCase):

  def testBasic(self):
    """Checks that unconstrained parameters yield finite joint densities."""
    model = stochastic_volatility.StochasticVolatility(
        centered_returns=tf.convert_to_tensor([5., -2.1, 8., 4., 1.1]))
    self.validate_log_prob_and_transforms(
        model,
        sample_transformation_shapes=dict(
            identity={
                'persistence_of_volatility': [],
                'mean_log_volatility': [],
                'white_noise_shock_scale': [],
                'log_volatility': [5]
            }))

  def testDeferred(self):
    """Checks that the dataset is not prematurely materialized."""
    self.validate_deferred_materialization(
        stochastic_volatility.StochasticVolatility,
        centered_returns=tf.convert_to_tensor([5., -2.1, 8., 4., 1.1]))

  def testSP500Small(self):
    """Checks that unconstrained parameters yield finite joint densities."""
    model = (
        stochastic_volatility.StochasticVolatilitySP500Small())
    self.validate_log_prob_and_transforms(
        model,
        sample_transformation_shapes=dict(
            identity={
                'persistence_of_volatility': [],
                'mean_log_volatility': [],
                'white_noise_shock_scale': [],
                'log_volatility': [100]
            }),
        check_ground_truth_mean_standard_error=True,
        check_ground_truth_mean=True,
        check_ground_truth_standard_deviation=True)

  def testSP500(self):
    """Checks that unconstrained parameters yield finite joint densities."""
    model = (
        stochastic_volatility.StochasticVolatilitySP500())
    self.validate_log_prob_and_transforms(
        model,
        sample_transformation_shapes=dict(
            identity={
                'persistence_of_volatility': [],
                'mean_log_volatility': [],
                'white_noise_shock_scale': [],
                'log_volatility': [2516]
            }),
        check_ground_truth_mean_standard_error=True,
        check_ground_truth_mean=True,
        check_ground_truth_standard_deviation=True)

if __name__ == '__main__':
  tf.test.main()
