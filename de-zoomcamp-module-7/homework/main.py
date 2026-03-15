def main():
    print("Module 7 homework workspace is ready.")
    print("Use:")
    print("  uv run src/producers/producer_green.py")
    print("  uv run src/consumers/consumer_green.py")
    print("  docker compose up -d")
    print("  docker compose exec jobmanager flink run -py /opt/src/job/homework_job.py")


if __name__ == "__main__":
    main()
