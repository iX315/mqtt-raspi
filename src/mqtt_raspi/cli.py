import time
import argparse
from pi5neo import Pi5Neo
from effects import rainbow_cycle, solid, loading_bar, firework, temperature

# Initialize the Pi5Neo class with 12 LEDs and an SPI speed of 800kHz
neo = Pi5Neo('/dev/spidev0.0', 12, 800)

def main():
    parser = argparse.ArgumentParser(description="Fan Led tool (argb) connect it to SPI pin (rpi5 SPI0 MOSI).")

    parser.add_argument('preset', type=str, choices=['rainbow_cycle', 'solid', 'loading_bar', 'firework', 'temperature'], help='run the selected preset')
    parser.add_argument('--delay', type=float, nargs='?', default=0.2, help='delay between color updates')
    parser.add_argument('--color', type=str, nargs='?', default="255,255,255", help='solid color: #hex r,g,b or name')
    parser.add_argument('--loop', action='store_true', help='run in loop')

    # Parse the arguments
    args = parser.parse_args()

    try:
        while True:
            if args.preset == 'rainbow_cycle':
                rainbow_cycle(neo, args.delay)
            elif args.preset == 'solid':
                solid(neo, args.color)
            elif args.preset == 'loading_bar':
                loading_bar(neo, args.delay, args.color)
            elif args.preset == 'firework':
                firework(neo, args.delay)
            elif args.preset == 'temperature':
                temperature(neo)
            if not args.loop:
                break  # Exit the loop if not in loop mode
            time.sleep(args.delay)  # Optional: Add a delay to prevent rapid looping

    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
