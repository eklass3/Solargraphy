from crontab import CronTab

cron = CronTab(user='pi')
job = cron.new(command='python /home/pi/Solargraphy/IntensityDetector.py')
job.minute.every(1)

cron.write()