import sys
from pathlib import Path

# Add the package to path
sys.path.insert(0, str(Path(__file__).parent))

from damngood.mcp_manager import main

if __name__ == "__main__":
    main()
