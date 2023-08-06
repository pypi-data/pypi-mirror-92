import numpy as np
from napari_demo import napari_experimental_provide_function
from napari_demo.napari_demo import Operation


def test_function():
    function = napari_experimental_provide_function()
    assert callable(function)

    # load all files into array
    arrays = np.ones((4, 4))
    # stack arrays into single array
    data = np.squeeze(np.stack(arrays))

    # make sure we're delivering the right format
    layer_data = function(data, Operation.subtract, data)
    assert len(layer_data) == 4
    assert (layer_data == np.zeros((4, 4))).all()
