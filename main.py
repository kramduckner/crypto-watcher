from button_thread import buttonThread
from price_updater_thread import priceUpdaterThread

def main():
    price_updater_thread = priceUpdaterThread(1, "price_updater_thread", 5)
    button_input_thread = buttonThread(2,'button_input_thread', 2)
    price_updater_thread.start()
    button_input_thread.start()

if __name__ == "__main__":
    main()
