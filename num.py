import base64
import re
import platform
import os
import json
import time

print("[*] Checking Requirements Module.....")
if platform.system().startswith("Linux"):
    try:
        import requests
    except ImportError:
        os.system("python3 -m pip install requests -q -q -q")
        import requests
    try:
        from pystyle import *
    except:
        os.system("python3 -m pip install pystyle -q -q -q")
        from pystyle import *
    try:
        import colorama
        from colorama import Fore, Back, Style
    except ImportError:
        os.system("python3 -m pip install colorama -q -q -q")
        import colorama
        from colorama import Fore, Back, Style

elif platform.system().startswith("Windows"):
    try:
        import requests
    except ImportError:
        os.system("python -m pip install requests -q -q -q")
        import requests
    try:
        import colorama
        from colorama import Fore, Back, Style
    except ImportError:
        os.system("python -m pip install colorama -q -q -q")
        import colorama
        from colorama import Fore, Back, Style
    try:
        from pystyle import *
    except:
        os.system("python -m pip install pystyle -q -q -q")
        from pystyle import *

colorama.init()

banner = Center.XCenter(r"""********************************************************************
*     _    _          _____ _  ______   _ _    _ __  __            *
*    | |  | |   /\   / ____| |/ / __ \ | | |  | |  \/  |           *
*    | |__| |  /  \ | |    | ' / |  | \| | |  | | \  / |           *
*    |  __  | / /\ \| |    |  <| |  | | | | |  | | |\/| |          *
*    | |  | |/ ____ \ |____| . \ |__| | | | |__| | |  | |          *
*    |_|  |_/_/    \_\_____|_|\_\____/ |_|\____/|_|  |_|           *
*                                                                  *
*           ADVANCED PHONE NUMBER INTEL AND VALIDATION TOOL        *
*                                                                  *
*                    Enhanced Version v5.0                         *
*                    Coded By: Bamitstech                          *
*********************************************************************
          Note: Enter Number with country code but without +
                          (233599788509)
""")

def clear_screen():
    os_name = "cls" if platform.system() == "Windows" else "clear"
    os.system(os_name)

def print_banner():
    clear_screen()
    print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))

def is_valid_mobile_number(mobile_number):
    # Enhanced validation for multiple countries
    patterns = {
        'Ghana': r"^233[2-7][0-9]{8}$",
        'Nigeria': r"^234[7-9][0-9]{9}$",
        'US': r"^1[2-9][0-9]{9}$",
        'UK': r"^44[1-9][0-9]{8,9}$",
        'General': r"^[1-9][0-9]{7,14}$"  # General international format
    }
    
    for country, pattern in patterns.items():
        if re.match(pattern, mobile_number):
            return True, country
    return False, None

def get_carrier_info(number):
    """Get carrier information using multiple APIs"""
    try:
        # APILayer Number Verification
        message = base64.b64decode(
            'aHR0cHM6Ly9hcGkuYXBpbGF5ZXIuY29tL251bWJlcl92ZXJpZmljYXRpb24vdmFsaWRhdGU/bnVtYmVyPQ=='.encode(
                'ascii')).decode('ascii')
        url = f"{message}{number}"
        hello = base64.b64decode('dGdDckRFOVF0QVF4Q1lvNnk4dHprMUdtQTJKbzBYZmI='.encode('ascii')).decode('ascii')
        
        headers = {"apikey": hello}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(Fore.RED + f"[!] Error getting carrier info: {str(e)}")
        return None

def get_geolocation_info(country_code, number, enhanced=False):
    """Get approximate geolocation using OpenCage Geocoding"""
    try:
        if not enhanced:
            # Basic geolocation for regular lookup
            mock_geo_data = {
                "approximate_location": "Regional area (precise location not available)",
                "timezone": "GMT+0",
                "region": "Unknown",
                "coordinates": "Approximate coordinates not available system are way safer nowadays"
            }
            return mock_geo_data
        else:
            # Enhanced geolocation using OpenCage API
            api_key = "e7e81edf1da64b29a4abd72e40b41be2"  # Using the API key directly
            if not api_key:
                print(Fore.RED + "[!] OpenCage API key not found.")
                return None

            # Get carrier info first
            carrier_data = get_carrier_info(number)
            if not carrier_data:
                print(Fore.RED + "[!] Unable to get initial carrier data for geolocation.")
                return None

            # Use OpenCage API to get detailed location
            base_url = "https://api.opencagedata.com/geocode/v1/json"
            # Use the API key directly if provided in code
            api_key = "e7e81edf1da64b29a4abd72e40b41be2"
            query = f"{carrier_data.get('location', '')} {carrier_data.get('country_name', '')}"
            
            params = {
                'q': query,
                'key': api_key,
                'language': 'en',
                'limit': 1
            }
            
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                result = response.json()
                if result['results']:
                    location = result['results'][0]
                    return {
                        "approximate_location": location['formatted'],
                        "timezone": location.get('annotations', {}).get('timezone', {}).get('name', 'Unknown'),
                        "region": location.get('components', {}).get('state', 'Unknown'),
                        "coordinates": f"{location['geometry']['lat']}, {location['geometry']['lng']}",
                        "confidence": location['confidence'],
                        "bounds": location.get('bounds', {}),
                        "address_components": location.get('components', {}),
                        "additional_info": {
                            "currency": location.get('annotations', {}).get('currency', {}),
                            "flag": location.get('annotations', {}).get('flag', ''),
                            "country_calling_code": location.get('annotations', {}).get('callingcode', '')
                        }
                    }
            return None
    except Exception as e:
        print(Fore.YELLOW + f"[!] Enhanced geolocation lookup failed: {str(e)}")
        return None

def generate_map_html(coordinates, location_name):
    """Generate HTML file with map"""
    try:
        lat, lng = map(float, coordinates.split(','))
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Location Map - {location_name}</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"/>
            <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
            <style>
                #map {{ height: 500px; width: 100%; }}
                body {{ margin: 0; padding: 20px; font-family: Arial, sans-serif; }}
                .info {{ margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="info">
                <h2>📍 Location Information</h2>
                <p><strong>Location:</strong> {location_name}</p>
                <p><strong>Coordinates:</strong> {coordinates}</p>
            </div>
            <div id="map"></div>
            <script>
                var map = L.map('map').setView([{lat}, {lng}], 13);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors'
                }}).addTo(map);
                L.marker([{lat}, {lng}]).addTo(map)
                    .bindPopup("{location_name}")
                    .openPopup();
            </script>
        </body>
        </html>
        """
        
        # Create maps directory if it doesn't exist
        if not os.path.exists('maps'):
            os.makedirs('maps')
            
        # Save HTML file
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"maps/location_map_{timestamp}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return filename
    except Exception as e:
        print(Fore.RED + f"[!] Error generating map: {str(e)}")
        return None

def enhanced_geolocation_tracking():
    """Handle enhanced geolocation tracking"""
    print(Fore.CYAN + "\n[*] Enhanced Geolocation Tracking Mode")
    print(Fore.YELLOW + "[!] Note: This provide you with precise location")
    print(Fore.YELLOW + "[*] Track number now🤣🤣🤣🥰")
    
    mobile_number = input(Fore.GREEN + '[+] Enter Phone Number: ').strip()
    if not mobile_number:
        print(Fore.RED + '[!] No number entered.')
        return
    
    is_valid, detected_country = is_valid_mobile_number(mobile_number)
    if not is_valid:
        print(Fore.RED + '[!] Invalid Mobile Number Format.')
        return
    
    print(Fore.GREEN + f'[+] Valid number detected (Format: {detected_country})')
    print(Fore.YELLOW + '[*] Gathering enhanced location intelligence...')
    
    carrier_data = get_carrier_info(mobile_number)
    if carrier_data:
        geo_data = get_geolocation_info(
            carrier_data.get('country_code', ''),
            mobile_number,
            enhanced=True
        )
        
        if geo_data:
            print(Fore.CYAN + "\n" + "="*60)
            print(Fore.CYAN + "           ENHANCED GEOLOCATION REPORT")
            print(Fore.CYAN + "="*60)
            print(Fore.GREEN + f"📱 Number: {mobile_number}")
            print(Fore.GREEN + f"📍 Location: {geo_data['approximate_location']}")
            print(Fore.GREEN + f"🌐 Coordinates: {geo_data['coordinates']}")
            print(Fore.GREEN + f"🕒 Timezone: {geo_data['timezone']}")
            print(Fore.GREEN + f"🏢 Region: {geo_data['region']}")
            
            if 'additional_info' in geo_data:
                print(Fore.YELLOW + "\n[+] Additional Information:")
                if 'currency' in geo_data['additional_info']:
                    print(Fore.YELLOW + f"💰 Currency: {geo_data['additional_info']['currency'].get('name', 'Unknown')}")
                if 'flag' in geo_data['additional_info']:
                    print(Fore.YELLOW + f"🏳️ Country Flag: {geo_data['additional_info']['flag']}")
            
                # Generate and open map HTML file
                map_file = generate_map_html(geo_data['coordinates'], geo_data['approximate_location'])
                if map_file:
                    abs_path = os.path.abspath(map_file)
                    print(Fore.GREEN + "\n[+] Map Generated Successfully!")
                    print(Fore.YELLOW + "[*] Opening map in your default browser...")
                    # Open the map in default browser
                    import webbrowser
                    webbrowser.open('file:///' + abs_path.replace('\\', '/'))            
                    print(Fore.RED + "\n⚠️ Privacy Notice:")
            print(Fore.RED + "   Lets break rules, and create the one that fits us.")
            print(Fore.RED + "   Lets hack🤣.")
            print(Fore.CYAN + "="*60)
        else:
            print(Fore.RED + '[!] Unable to retrieve enhanced location data.')
    else:
        print(Fore.RED + '[!] Unable to retrieve carrier information.')

def get_device_info(line_type):
    """Determine likely device type based on line type"""
    device_mapping = {
        "mobile": "Mobile Phone/Smartphone",
        "landline": "Landline/Fixed Phone",
        "voip": "VoIP Service/Internet Phone",
        "toll_free": "Toll-free Service Number",
        "premium": "Premium Rate Number"
    }
    return device_mapping.get(line_type.lower(), "Unknown Device Type")

def format_results(data, geo_data):
    """Format and display results in a structured way"""
    print(Fore.CYAN + "\n" + "="*60)
    print(Fore.CYAN + "           PHONE NUMBER INTELLIGENCE REPORT")
    print(Fore.CYAN + "="*60)
    
    if data:
        print(Fore.GREEN + f"📱 Number: {data.get('number', 'N/A')}")
        print(Fore.GREEN + f"🌍 Country: {data.get('country_name', 'N/A')} ({data.get('country_code', 'N/A')})")
        print(Fore.GREEN + f"📞 International Format: {data.get('international_format', 'N/A')}")
        print(Fore.GREEN + f"📱 Local Format: {data.get('local_format', 'N/A')}")
        print(Fore.GREEN + f"📡 Line Type: {data.get('line_type', 'N/A')}")
        print(Fore.GREEN + f"🔧 Device Type: {get_device_info(data.get('line_type', ''))}")
        print(Fore.GREEN + f"✅ Valid: {data.get('valid', 'N/A')}")
        
        carrier = data.get('carrier', 'N/A')
        if carrier and carrier != 'N/A':
            print(Fore.YELLOW + f"📶 Carrier: {carrier}")
        else:
            print(Fore.YELLOW + f"📶 Carrier: Not available")
        
        if geo_data:
            print(Fore.BLUE + f"📍 Location: {geo_data.get('approximate_location', 'N/A')}")
            print(Fore.BLUE + f"🕐 Timezone: {geo_data.get('timezone', 'N/A')}")
            print(Fore.BLUE + f"🏢 Region: {geo_data.get('region', 'N/A')}")
    
    print(Fore.RED + "\n⚠️  PRIVACY NOTICE:")
    print(Fore.RED + "   Personal information (names, exact addresses) is not")
    print(Fore.RED + "   provided to protect user privacy and comply with regulations.")
    print(Fore.CYAN + "="*60)

def show_menu():
    print(Fore.YELLOW + "\n" + "="*40)
    print(Fore.YELLOW + "           MAIN MENU")
    print(Fore.YELLOW + "="*40)
    print(Fore.GREEN + "1. Lookup Phone Number")
    print(Fore.GREEN + "2. Batch Lookup (Multiple Numbers)")
    print(Fore.GREEN + "3. View Supported Countries")
    print(Fore.GREEN + "4. Enhanced Geolocation Tracking")
    print(Fore.RED + "0. Exit")
    print(Fore.YELLOW + "="*40)

def batch_lookup():
    """Handle multiple number lookups"""
    print(Fore.CYAN + "\n[*] Batch Lookup Mode")
    print(Fore.YELLOW + "[*] Enter phone numbers one by one (press Enter with empty input to finish)")
    
    numbers = []
    while True:
        number = input(Fore.GREEN + f"[+] Enter Phone Number #{len(numbers)+1} (or press Enter to finish): ").strip()
        if not number:
            break
        numbers.append(number)
    
    if not numbers:
        print(Fore.RED + "[!] No numbers entered.")
        return
    
    print(Fore.CYAN + f"\n[*] Processing {len(numbers)} numbers...")
    for i, number in enumerate(numbers, 1):
        print(Fore.YELLOW + f"\n--- Processing Number {i}/{len(numbers)} ---")
        process_single_number(number)
        if i < len(numbers):
            time.sleep(1)  # Rate limiting

def show_supported_countries():
    """Display supported country codes"""
    countries = {
        "233": "Ghana",
        "234": "Nigeria", 
        "1": "United States/Canada",
        "44": "United Kingdom",
        "27": "South Africa",
        "254": "Kenya",
        "256": "Uganda"
    }
    
    print(Fore.CYAN + "\n" + "="*40)
    print(Fore.CYAN + "      SUPPORTED COUNTRIES")
    print(Fore.CYAN + "="*40)
    for code, country in countries.items():
        print(Fore.GREEN + f"{code:4} - {country}")
    print(Fore.CYAN + "="*40)
    print(Fore.YELLOW + "\nNote: Tool works with most international numbers")

def process_single_number(mobile_number):
    """Process a single phone number lookup"""
    is_valid, detected_country = is_valid_mobile_number(mobile_number)
    
    if not is_valid:
        print(Fore.RED + '[!] Invalid Mobile Number Format.')
        print(Fore.YELLOW + '[*] Please ensure you include the country code without + sign')
        print(Fore.YELLOW + '[*] Example: 2335000000000 (Ghana), 1234567890 (US)')
        return False
    
    print(Fore.GREEN + f'[+] Valid number detected (Format: {detected_country})')
    print(Fore.YELLOW + '[*] Gathering intelligence...')
    
    # Get carrier and basic info
    carrier_data = get_carrier_info(mobile_number)
    
    if carrier_data:
        # Get geolocation info
        geo_data = get_geolocation_info(
            carrier_data.get('country_code', ''), 
            mobile_number
        )
        
        # Display formatted results
        format_results(carrier_data, geo_data)
        return True
    else:
        print(Fore.RED + '[!] Unable to retrieve number information.')
        print(Fore.YELLOW + '[*] This might be due to API limits or invalid number.')
        return False

def main():
    """Main application loop"""
    try:
        while True:
            print_banner()
            show_menu()
            
            choice = input(Fore.GREEN + '\n[+] Select an option: ').strip()
            
            if choice == '0':
                print(Fore.YELLOW + '\n[*] Thank you for using HACKIUM Phone Intel Tool!')
                print(Fore.YELLOW + '[*] Exiting...')
                break
            
            elif choice == '1':
                print(Fore.CYAN + '\n[*] Single Number Lookup Mode')
                mobile_number = input(Fore.GREEN + '[+] Enter Mobile Number: ').strip()
                
                if mobile_number:
                    process_single_number(mobile_number)
                else:
                    print(Fore.RED + '[!] No number entered.')
                
                input(Fore.YELLOW + '\n[*] Press Enter to continue...')
            
            elif choice == '2':
                batch_lookup()
                input(Fore.YELLOW + '\n[*] Press Enter to continue...')
            
            elif choice == '3':
                show_supported_countries()
                input(Fore.YELLOW + '\n[*] Press Enter to continue...')
            
            elif choice == '4':
                enhanced_geolocation_tracking()
                input(Fore.YELLOW + '\n[*] Press Enter to continue...')
            
            else:
                print(Fore.RED + '[!] Invalid option. Please select 0-4.')
                time.sleep(1)
    
    except KeyboardInterrupt:
        print(Fore.RED + '\n\n[*] Program interrupted by user.')
        print(Fore.YELLOW + '[*] Exiting gracefully...')
    except Exception as e:
        print(Fore.RED + f'\n[!] An unexpected error occurred: {str(e)}')
        print(Fore.YELLOW + '[*] Please try again.')

if __name__ == "__main__":
    main()