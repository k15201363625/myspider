from proxypool.scheduler import Scheduler

def main():
    try:
        scheduler = Scheduler()
        scheduler.scheduler_run()
    except Exception as e:
        print(e.args)
        print('--------------------------------------------')
        print('retry to start the proxy pool')
        main()


if __name__ == '__main__':
    main()
