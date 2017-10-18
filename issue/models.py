from django.db import models

# Create your models here.


class IssueRecord(models.Model):
    project_name = models.CharField("工程名", max_length=100)
    issue_content = models.CharField("发布内容",max_length=500,null=True)
    issue_time = models.DateTimeField(null=True)
    dev_person = models.CharField("开发人员",max_length=100,null=True)
    test_person = models.CharField("测试人员",max_length=100,null=True)
    issue_person = models.CharField("发布人员",max_length=100,null=True)
    issue_status = models.CharField("发布状态",max_length=3,default="0")
    svn_path = models.CharField("svn路径",max_length=500,null=True)
    remark = models.CharField("备注信息",max_length=500,null=True)

    class Meta:
        db_table = 'issue_issuerecord'
        ordering = ['id']

    def __str__(self):
        return self.issue_content

# 测试数据、
'''
from issue.models import IssueRecord
import datetime
data={"project_name":"front","issue_content":"测试页面","issue_time":datetime.datetime.now(),"dev_person":"金","test_person":"黄龙","issue_person":"发布人员","remark":"备注信息"}
for i in range(1,10000):
    nice = IssueRecord(**data)
    nice.save()
'''









