import pytest
import tempfile
import shutil
import numpy as np
from pathlib import Path
from unittest.mock import Mock, MagicMock

from triangler.config import TrianglerConfig


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_image():
    """Create a simple test image as numpy array."""
    # Create a simple 100x100 RGB image with some pattern
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    # Add some pattern to make it interesting
    image[25:75, 25:75, 0] = 255  # Red square
    image[40:60, 40:60, 1] = 255  # Green square in center
    return image


@pytest.fixture
def sample_grayscale_image():
    """Create a simple grayscale test image as numpy array."""
    image = np.zeros((50, 50), dtype=np.uint8)
    image[10:40, 10:40] = 128  # Gray square
    image[20:30, 20:30] = 255  # White square in center
    return image


@pytest.fixture
def sample_image_file(temp_dir, sample_image):
    """Create a temporary image file."""
    import imageio
    image_path = temp_dir / "test_image.png"
    imageio.imwrite(str(image_path), sample_image)
    return image_path


@pytest.fixture
def sample_output_file(temp_dir):
    """Provide a path for test output files."""
    return temp_dir / "output.png"


@pytest.fixture
def default_config():
    """Create a default TrianglerConfig for testing."""
    return TrianglerConfig()


@pytest.fixture
def custom_config():
    """Create a custom TrianglerConfig with specific settings."""
    config = TrianglerConfig()
    config.n_samples = 500
    return config


@pytest.fixture
def mock_edge_detector():
    """Mock edge detector for testing."""
    mock = Mock()
    mock.detect.return_value = np.array([[10, 10], [20, 20], [30, 30]])
    return mock


@pytest.fixture
def mock_sampler():
    """Mock sampler for testing."""
    mock = Mock()
    mock.sample.return_value = np.array([[5, 5], [15, 15], [25, 25], [35, 35]])
    return mock


@pytest.fixture
def mock_renderer():
    """Mock renderer for testing."""
    mock = Mock()
    mock.render.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    return mock


@pytest.fixture
def mock_scipy_spatial():
    """Mock scipy.spatial.Delaunay for testing."""
    mock_delaunay = MagicMock()
    mock_delaunay.simplices = np.array([[0, 1, 2], [1, 2, 3]])
    with pytest.mock.patch('scipy.spatial.Delaunay', return_value=mock_delaunay):
        yield mock_delaunay


@pytest.fixture
def mock_imageio():
    """Mock imageio functions for testing."""
    with pytest.mock.patch('imageio.imread') as mock_imread, \
         pytest.mock.patch('imageio.imwrite') as mock_imwrite:
        mock_imread.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
        yield {'imread': mock_imread, 'imwrite': mock_imwrite}


@pytest.fixture
def points_array():
    """Sample points array for testing triangulation."""
    return np.array([
        [0, 0], [100, 0], [0, 100], [100, 100],
        [50, 25], [25, 50], [75, 75], [50, 50]
    ], dtype=float)


@pytest.fixture
def triangles_array():
    """Sample triangles array for testing rendering."""
    return np.array([
        [0, 1, 4], [0, 4, 5], [1, 2, 4],
        [2, 3, 6], [4, 5, 6], [5, 6, 7]
    ])


@pytest.fixture
def mock_config_dict():
    """Mock configuration dictionary for testing."""
    return {
        'points': 1000,
        'outline': 0,
        'blur': 0,
        'edge_detector': 'canny',
        'sampler': 'poisson',
        'renderer': 'centroid'
    }


@pytest.fixture(autouse=True)
def reset_random_seed():
    """Reset random seed before each test for reproducible results."""
    np.random.seed(42)


class MockImageFile:
    """Mock image file class for testing file operations."""
    def __init__(self, width=100, height=100, channels=3):
        self.width = width
        self.height = height
        self.channels = channels
        self.data = np.random.randint(0, 256, (height, width, channels), dtype=np.uint8)
    
    def read(self):
        return self.data


@pytest.fixture
def mock_image_file():
    """Create a mock image file object."""
    return MockImageFile()


@pytest.fixture
def large_image():
    """Create a larger test image for integration tests."""
    return np.random.randint(0, 256, (500, 500, 3), dtype=np.uint8)


@pytest.fixture
def edge_points():
    """Sample edge points for testing edge detection."""
    return np.array([
        [10, 10], [20, 10], [30, 10],
        [10, 20], [30, 20],
        [10, 30], [20, 30], [30, 30]
    ])


@pytest.fixture
def color_samples():
    """Sample colors for testing rendering."""
    return np.array([
        [255, 0, 0],    # Red
        [0, 255, 0],    # Green
        [0, 0, 255],    # Blue
        [255, 255, 0],  # Yellow
        [128, 128, 128] # Gray
    ], dtype=np.uint8)