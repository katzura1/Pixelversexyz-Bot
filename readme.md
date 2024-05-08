# PixelverseXYZ Clicker Bot
[![App Screenshot](https://raw.githubusercontent.com/katzura1/Pixelversexyz-Bot/main/SCR-20240508-ste.png)](https://raw.githubusercontent.com/katzura1/Pixelversexyz-Bot/main/SCR-20240508-ste.png)


This script automates clicks in the PixelverseXYZ app. It uses the developer console to identify and extract necessary tokens and modifies the script to automate the clicker functionality.

## Step-by-Step Instructions

1. **Open the Developer Console**
   - In your web browser, open the developer tools (usually accessed with `F12` or `Ctrl+Shift+I`).
   - Go to the "Network" tab to inspect network requests.

2. **Open the PixelverseXYZ App**
   - Navigate to the PixelverseXYZ app or website in your browser to start capturing network traffic.

3. **Extract TGID and Secret**
   - Look for HTTP requests to the following endpoint: `https://api-clicker.pixelverse.xyz/api/users`.
   - Identify the request that contains the `tgid` and `secret`.
   - These values may be present in the request headers or the URL itself.

4. **Edit the Script**
   - Open the script file `main.py`.
   - Update the placeholders for `tgid` and `secret` with the extracted information from step 3.

5. **Run the Script**
   - Ensure Python is installed on your system.
   - Open a terminal or command prompt in the directory where `main.py` is located.
   - Execute the script with the following command:
     ```bash
     python main.py
     ```

## Troubleshooting

- **Incorrect TGID or Secret:** Double-check the extracted values to ensure they are accurate and placed in the correct locations within the script.
- **Python Not Found:** Confirm that Python is installed on your system and properly added to the PATH.
- **Script Errors:** If the script encounters issues, refer to the error messages for clues, and ensure all required information is correctly entered.

## Disclaimer

This script is for educational and personal use only. Ensure you have permission to use any tools or applications involved. Unauthorized use or accessing services without authorization may violate terms of service or laws. Use this script responsibly and at your own risk.

## License

This script is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute it, but must provide attribution to the original author.

