import asyncio
import sys
import os # Import the operating system module
from avwx import Metar

# NOTE: avwx is an asynchronous library, so we define the fetching function as async.

def clear_screen():
    """Clears the console screen based on the operating system."""
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Linux and macOS
    else:
        os.system('clear')

async def run_continuous_fetch(station_icao: str):
    """
    Continuously fetches and displays the latest raw METAR data every minute.

    :param station_icao: The ICAO code of the airport (e.g., 'KORD', 'EGLL').
    """
    station_icao = station_icao.upper()

    while True:
        # Clear the screen before fetching and printing the new data
        clear_screen()
        
        print(f"\n--- Fetching METAR for {station_icao} ---")
        
        try:
            # 1. Initialize the Metar object with the station ICAO code.
            metar_report = Metar(station_icao)

            # 2. Use the instance method async_update() to fetch and parse the data.
            await metar_report.async_update()

            # SUCCESS CHECK: We check for the presence of the 'raw' report string.
            if metar_report.raw:
                #print("\n[Raw METAR String]")
                print(metar_report.raw)
            # FAILURE/NO DATA CASE: If the raw report is empty, it means no data was found.
            else:
                 print(f"\nNo recent METAR data found or available for {station_icao}.")

        except Exception as e:
            # If an error occurs (e.g., network issue), print it and continue the loop.
            print(f"\nAn unexpected error occurred while processing data: {e}")
            print("Will retry in 60 seconds.")

        # Wait for 60 seconds before the next loop iteration (refresh).
        print("\n--- Waiting 60 seconds for next refresh ---")
        await asyncio.sleep(60)


if __name__ == "__main__":
    icao_code = ""
    # Check if ICAO code was passed as a command-line argument
    if len(sys.argv) > 1:
        icao_code = sys.argv[1]
    else:
        # Prompt user if no argument was provided
        icao_code = input("Enter the 4-letter ICAO airport code (e.g., KORD, EGLL): ")

    # Ensure the input is not empty before starting the loop
    if not icao_code:
        print("\nError: ICAO code cannot be empty. Exiting.")
        sys.exit(1)

    print(f"Starting continuous METAR fetch for {icao_code.upper()}. Press Ctrl+C to stop.")
    
    # Run the continuous fetcher function
    try:
        asyncio.run(run_continuous_fetch(icao_code))
    except KeyboardInterrupt:
        print("\nMETAR fetch stopped by user.")
