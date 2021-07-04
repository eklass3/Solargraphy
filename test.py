from crontab import CronTab

cron = CronTab()

job = cron.new(command='python /home/pi/Merger/IntensityDetector.py')

job.minute.every(2)

cron.write()
