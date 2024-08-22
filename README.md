# flipdotapi 🌟

## Summary of Project 📖

Welcome to **flipdotapi**! This repository contains a Python library designed to interact seamlessly with a flip-dot sign server. The core of this library is built around the ability to render and manage text and images on a flip-dot display, facilitating dynamic messaging and eye-catching presentations. Whether you're looking to display simple messages or creative designs, flipdotapi provides a flexible and intuitive interface for achieving your goals! 🚀

## How to Use 🔧

### Installation

Make sure you have Python 3.6 or higher installed. You can install the required libraries using pip:

```bash
pip install -r requirements.txt
```

### Basic Example

Here’s a quick guide on how to set up a basic flip-dot display:

1. **Initialization**: Start by creating an instance of the `remote_sign` class from the flipdotapi.

    ```python
    from flipdotapi import remote_sign as sign

    sign_url = "http://your-flipdot-server/api/dots"  # Update with your server URL
    sign_columns = 96
    sign_rows = 16
    sign_sim = False  # Set to True to use the simulator

    flipdot_display = sign(sign_url, sign_columns, sign_rows, simulator=sign_sim)
    ```

2. **Displaying Text**: Use the `write_text` method to display messages.

    ```python
    flipdot_display.write_text("Hello, Flip Dot!", alignment="center")
    ```

3. **Rendering Images**: Create a numpy array representing the desired image and use the `render_image` method.

    ```python
    import numpy as np

    img_array = np.zeros((sign_rows, sign_columns), dtype=np.uint8)
    # Modify img_array to create your desired image...
  
    flipdot_display.render_image(img_array)
    ```

### Example Scripts

Check out the provided example scripts, like `example.py` and `checkerboard.py`, for more detailed demonstrations of usage! 

## Tech Info 💻

- **Language**: Python 3
- **Dependencies**:
  - [Pillow](https://python-pillow.org/): For image processing and drawing text
  - [numpy](https://numpy.org/): Essential for array operations
  - [requests](https://docs.python-requests.org/en/master/): For making HTTP requests to the flip-dot API

### Structure Overview

The repository consists of various files, distributed as follows:

```
flipdotapi/
├── LICENSE
├── MANIFEST.in
├── README.md
├── checkerboard.py
├── example.py
├── flipdotapi/
│   ├── __init__.py
│   ├── simulator.py
│   └── text_builder.py
├── image.py
├── requirements.txt
├── setup.py
└── test-font.py
```

- The `flipdotapi` directory contains the core library files, including the simulator for testing without a physical sign.
- `example.py`, `checkerboard.py`, and `image.py` provide samples for how to implement various features.
- `setup.py` contains configuration information for packaging the library for distribution.

### License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to contribute to the project! If you encounter any issues or have suggestions, don't hesitate to open an issue or submit a pull request. Let's create amazing flip-dot experiences together! 🎉 

For further information and updates, check out the official GitHub repository at [harperreed/flipdotapi](https://github.com/harperreed/flipdotapi).
