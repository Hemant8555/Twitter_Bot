from django.shortcuts import render, redirect
from django.http import HttpResponse
import tweepy
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tweepy.error import TweepError

auth = tweepy.OAuthHandler("xxxxxxxxxxxxx","xxxxxxxxxxxxx")
auth.set_access_token("xxxxxxxxxxxxxxx-xxxxxxxxxxxxxx","xxxxxxxxxxxxxxxxx")
api = tweepy.API(auth,wait_on_rate_limit=True)

# Create your views here.
def index(request):
 if request.method == 'POST':
  index.query = request.POST['searchquery']
  try:
    search_user = api.get_user(index.query)
  except:
    return render(request,'no-data.html')
  get_tweets = api.user_timeline(screen_name=index.query,count=10)
  followers=api.followers(screen_name=index.query,count=15)

  if(search_user.followers_count > 10):
    left_followers = search_user.followers_count-10
  else:
    left_followers=0
  if(search_user.statuses_count > 10):
    left_tweets = search_user.statuses_count-10  
  else:
    left_tweets=0
  return render(request,'data.html',{'f_count':search_user.followers_count,
    'status_count':search_user.statuses_count,
    'get_tweets':get_tweets,
    'screen_name':search_user.name,
    'description':search_user.description,
    'followers':followers,
    'username':index.query,
    'left_tweets':left_tweets,
    'left_followers':left_followers})
 else:
  return render(request,'index.html')
 
def export_csv(request):
  if request.method == "POST":
    user_email = request.POST.get('useremail',False)
    followers_count = request.POST.get('followers_count',False)

    with open('follower.csv','w',newline='',encoding='utf-8') as csvfile:
      wrt = csv.writer(csvfile)
      for i in tweepy.Cursor(api.followers, index.query).items(int(followers_count)):
        n = i.name
        wrt.writerow([n])
      
      email_user = 'xxxx@x.xcom'
      email_password = 'xxxxxxxxxxxxxx'
      email_send = user_email

      subject = 'Followers csv file'

      msg = MIMEMultipart()
      msg['From'] = email_user
      msg['To'] = email_send
      msg['Subject'] = subject

      body = 'Hi there, Here is your followers file. Thanks for choosing us'
      msg.attach(MIMEText(body,'plain'))

      filename='follower.csv'
      attachment = open(filename,'rb')

      part = MIMEBase('application','octet-stream')
      part.set_payload((attachment).read())
      encoders.encode_base64(part)
      part.add_header('Content-Disposition',"attachment; filename= "+filename)

      msg.attach(part)
      text = msg.as_string()
      server = smtplib.SMTP('smtp.gmail.com',587)
      server.starttls()
      server.login(email_user,email_password)

      server.sendmail(email_user,email_send,text)
      server.quit()
    return redirect('')


  else:
    return redirect('/')


def export_csv_tweets(request):
  if request.method == "POST":
    user_email = request.POST.get('useremail',False)
    tweet_count = request.POST.get('tweet_count',False)

    with open('tweets.csv','w',newline='',encoding="utf-8") as csvfile:
      wrt = csv.writer(csvfile)
      for i in tweepy.Cursor(api.user_timeline, index.query).items(int(tweet_count)):
        n = i.text
        wrt.writerow([n])

      email_user = 'xxxxxxxx@xxxxx'
      email_password = 'xxxxxxxx'
      email_send = user_email

      subject = 'Tweets csv file'

      msg = MIMEMultipart()
      msg['From'] = email_user
      msg['To'] = email_send
      msg['Subject'] = subject

      body = 'Hi there, Here is your file. Thanks for choosing us'
      msg.attach(MIMEText(body,'plain'))

      filename='tweets.csv'
      attachment = open(filename,'rb')

      part = MIMEBase('application','octet-stream')
      part.set_payload((attachment).read())
      encoders.encode_base64(part)
      part.add_header('Content-Disposition',"attachment; filename= "+filename)

      msg.attach(part)
      text = msg.as_string()
      server = smtplib.SMTP('smtp.gmail.com',587)
      server.starttls()
      server.login(email_user,email_password)


      server.sendmail(email_user,email_send,text)
      server.quit()

    return HttpResponse('Your tweets file is sent to your email...')
  else:
    return redirect('/')
      

