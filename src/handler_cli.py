import argparse
from loguru import logger
from processors import get_default_processor_manager
from config import Config


import sentry_sdk

sentry_sdk.init(
    dsn=Config.SENTRY_DSN,
    integrations=[],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


def cli_handler():
    parser = argparse.ArgumentParser(description="Process a URL to generate audio.")
    parser.add_argument("url", type=str, help="The URL to process")
    parser.add_argument(
        "--output",
        type=str,
        default="out.mp3",
        help="The output file path to save the audio (default: out.mp3)",
    )
    args = parser.parse_args()

    try:
        processor_manager = get_default_processor_manager(
            store_base_path=Config.FS_STORE_DIR_PATH,
            gemini_api_key=Config.GEMINI_API_KEY,
            openai_api_key=Config.OPENAI_API_KEY,
        )
        logger.info(f"Processing URL from CLI: {args.url}")
        audio = processor_manager.process_event(args.url)
        logger.info(f"Successfully processed URL from CLI: {args.url}")
        with open(args.output, "wb") as f:
            f.write(audio)
        print(f"Audio has been successfully generated and saved as {args.output}")
    except Exception as e:
        print(f"Error processing request: {e}")


if __name__ == "__main__":
    cli_handler()
