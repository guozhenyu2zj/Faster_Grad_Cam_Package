import pytest
import numpy as np
from faster_grad_cam.grad_cam import FasterGradCam

fgc = FasterGradCam()

def test_process_image():
    '''
    Regression test.
    '''
    # Load the image
    image = np.random.randint(0, 256, size=(300, 300, 3), dtype=np.uint8)

    # Process the image and get the output
    hand1, color1, score1, image1 = fgc.process_image(image)
    hand2, color2, score2, image2 = fgc.process_image(image)

    # Check that the outputs are the same
    assert hand1 == hand2
    assert color1 == color2
    assert np.allclose(score1, score2)
    assert np.allclose(image1, image2)


def test_process_image_no_error():
    '''
    Load a big image and a small image
    '''
    big_image = np.random.randint(0, 256, size=(1000, 1000, 3), dtype=np.uint8)
    small_image = np.random.randint(0, 256, size=(10, 10, 3), dtype=np.uint8)

    # Process the big image and check that there are no errors
    try:
        fgc.process_image(big_image)
    except Exception as e:
        pytest.fail(f"Processing big image raised an exception: {e}")

    # Process the small image and check that there are no errors
    try:
        fgc.process_image(small_image)
    except Exception as e:
        pytest.fail(f"Processing small image raised an exception: {e}")
