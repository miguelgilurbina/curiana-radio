"""Configuración pytest: los módulos de curiana_sim viven en el directorio
padre (no es un paquete instalable), así que se agrega al sys.path."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
