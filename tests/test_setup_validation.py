"""
Validation tests to verify the testing infrastructure setup works correctly.
These tests ensure all components can be imported and basic functionality works.
"""

import pytest
import numpy as np
from pathlib import Path

# Test imports from the triangler package
def test_triangler_imports():
    """Test that all main triangler components can be imported."""
    from triangler import convert, TrianglerConfig
    from triangler.edge_detectors import EdgeDetector
    from triangler.renderers import Renderer
    from triangler.samplers import Sampler
    
    assert convert is not None
    assert TrianglerConfig is not None
    assert EdgeDetector is not None
    assert Renderer is not None
    assert Sampler is not None


def test_triangler_config_creation():
    """Test that TrianglerConfig can be created with default settings."""
    from triangler.config import TrianglerConfig
    
    config = TrianglerConfig()
    assert config is not None
    assert hasattr(config, 'n_samples')
    assert hasattr(config, 'edge_detector')
    assert hasattr(config, 'sampler')
    assert hasattr(config, 'renderer')
    assert config.n_samples == 1024


def test_pytest_fixtures(sample_image, temp_dir, default_config):
    """Test that pytest fixtures from conftest.py work correctly."""
    # Test sample image fixture
    assert isinstance(sample_image, np.ndarray)
    assert sample_image.shape == (100, 100, 3)
    assert sample_image.dtype == np.uint8
    
    # Test temp directory fixture
    assert isinstance(temp_dir, Path)
    assert temp_dir.exists()
    
    # Test config fixture
    from triangler.config import TrianglerConfig
    assert isinstance(default_config, TrianglerConfig)


def test_mock_fixtures(mock_edge_detector, mock_sampler, mock_renderer):
    """Test that mock fixtures work correctly."""
    # Test mock edge detector
    result = mock_edge_detector.detect(np.zeros((10, 10)))
    assert isinstance(result, np.ndarray)
    mock_edge_detector.detect.assert_called_once()
    
    # Test mock sampler
    result = mock_sampler.sample(np.zeros((10, 10)), 10)
    assert isinstance(result, np.ndarray)
    mock_sampler.sample.assert_called_once()
    
    # Test mock renderer
    result = mock_renderer.render(np.zeros((10, 10, 3)), [], [])
    assert isinstance(result, np.ndarray)
    mock_renderer.render.assert_called_once()


@pytest.mark.unit
def test_unit_marker():
    """Test that unit marker works."""
    assert True


@pytest.mark.integration
def test_integration_marker():
    """Test that integration marker works."""
    assert True


@pytest.mark.slow
def test_slow_marker():
    """Test that slow marker works."""
    assert True


def test_numpy_dependency():
    """Test that numpy is available and working."""
    import numpy as np
    
    arr = np.array([1, 2, 3])
    assert arr.sum() == 6


def test_imageio_dependency():
    """Test that imageio is available."""
    import imageio
    assert hasattr(imageio, 'imread')
    assert hasattr(imageio, 'imwrite')


def test_scipy_dependency():
    """Test that scipy is available."""
    import scipy
    from scipy.spatial import Delaunay
    assert Delaunay is not None


def test_skimage_dependency():
    """Test that scikit-image is available."""
    import skimage
    from skimage import filters
    assert filters is not None


def test_file_operations(temp_dir, sample_image_file):
    """Test file operations with fixtures."""
    # Test that sample image file was created
    assert sample_image_file.exists()
    assert sample_image_file.suffix == '.png'
    
    # Test reading the image
    import imageio
    image = imageio.imread(str(sample_image_file))
    assert isinstance(image, np.ndarray)
    assert len(image.shape) == 3  # RGB image


def test_triangulation_basic():
    """Test basic triangulation functionality."""
    from scipy.spatial import Delaunay
    
    # Create some test points
    points = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
    tri = Delaunay(points)
    
    assert tri.simplices.shape[1] == 3  # Triangles have 3 vertices
    assert len(tri.simplices) > 0


def test_coverage_exclusions():
    """Test that coverage exclusions work by testing some excluded code patterns."""
    def test_function():
        if __name__ == "__main__":  # pragma: no cover
            pass
        
        if 0:  # pragma: no cover
            pass
            
        def __repr__(self):  # pragma: no cover
            return "test"
    
    # This test should pass even with the excluded lines
    assert test_function is not None