from brainflow import BrainFlowInputParams, BoardShim, BoardIds
import time
import numpy as np


# BoardShim.enable_dev_board_logger()

params = BrainFlowInputParams()
params.serial_port = "COM5"

board = BoardShim(BoardIds.CYTON_BOARD.value, params)

try:
    board.prepare_session()
    board.start_stream(1200)

    print("Starting data stream... Press Ctrl+C to stop.")
    
    while True:
        data = board.get_current_board_data(10)

        eeg_channels = data[:8, :]
        eeg_means = np.mean(eeg_channels, axis=1)
        
        print(f"\r{[f'{i}: {np.round(eeg_means, 3)[i]:8.3f}' for i in range(8)]}", end='', flush=True)

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nStopping data stream...")

finally:
    board.stop_stream()
    board.release_session()
    print("Session stopped.")
