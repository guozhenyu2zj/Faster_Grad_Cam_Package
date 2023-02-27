import pytest
import numpy as np
import numpy as np
from sklearn.externals import joblib
from faster_grad_cam.demo import *


# regression test
def test_process_image():
    # Load the image
    image = np.random.randint(0, 256, size=(300, 300, 3), dtype=np.uint8)

    # Process the image and get the output
    hand1, color1, score1, image1 = process_image(image)
    hand2, color2, score2, image2 = process_image(image)

    # Check that the outputs are the same
    assert hand1 == hand2
    assert color1 == color2
    assert np.allclose(score1, score2)
    assert np.allclose(image1, image2)

# no error test 
def test_process_image_no_error():
    # Load a big image and a small image
    big_image = np.random.randint(0, 256, size=(1000, 1000, 3), dtype=np.uint8)
    small_image = np.random.randint(0, 256, size=(10, 10, 3), dtype=np.uint8)

    # Process the big image and check that there are no errors
    try:
        output1 = process_image(big_image)
    except Exception as e:
        pytest.fail(f"Processing big image raised an exception: {e}")

    # Process the small image and check that there are no errors
    try:
        output2 = process_image(small_image)
    except Exception as e:
        pytest.fail(f"Processing small image raised an exception: {e}")