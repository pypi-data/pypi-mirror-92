import requests
import json
class fetch_user:
  def __init__(self,token,id):
    self.fetch=id
    self.headers={"Authorization":"Bot "+str(token)}
    self.base="https://discord.com/api/v7/users/"+str(id)
    self.res=requests.get(self.base,headers=self.headers)
    self.new=json.loads(self.res.content)
  def user(self):
    return self.new
  def id(self):
    return self.new["id"]
  def name(self):
    return self.new["username"]
  def avatar(self):
    return self.new["avatar"]
  def discriminator(self):
    return self.new["discriminator"]