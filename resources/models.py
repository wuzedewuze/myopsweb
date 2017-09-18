from django.db import models


# 机房信息
class Idc(models.Model):
    name = models.CharField("idc 字母简称", max_length=10, default="", unique=True)
    idc_name = models.CharField("idc 中文名字", max_length=100, default="")
    address = models.CharField("具体的地址，云厂商可以不填", max_length=255, null=True)
    phone = models.CharField("机房联系电话", max_length=20, null=True)
    email = models.EmailField("机房联系email", null=True)
    username  = models.CharField("机房联系人", max_length=32, null=True)

    class Meta:
        db_table = "resources_idc"
        permissions = (
            ("view_idc", "访问idc列表页面"),
        )


# 服务器信息模型
class Server(models.Model):
    supplier = models.IntegerField("供应商",null=True)
    manufacturers = models.CharField("生产厂商",max_length=50, null=True)
    manufacture_date = models.DateField("生产日期",null=True)
    server_type = models.CharField("服务器类型",max_length=20, null=True)
    sn = models.CharField("SN码",max_length=60, db_index=True, null=True)
    idc = models.ForeignKey(Idc, null=True)
    os = models.CharField("操作系统",max_length=50, null=True)
    hostname = models.CharField("主机名",max_length=50, db_index=True, null=True)
    inner_ip = models.CharField("管理ip",max_length=32, null=True, unique=True)
    mac_address = models.CharField("mac地址",max_length=50, null=True)
    ip_info = models.CharField("ip信息",max_length=255, null=True)
    server_cpu = models.CharField("cpu信息",max_length=250, null=True)
    server_disk = models.CharField("磁盘信息",max_length=100, null=True)
    server_mem = models.CharField("内存信息",max_length=100, null=True)
    status = models.CharField("服务器状态",max_length=100,db_index=True, null=True)
    remark = models.TextField(null=True)
    service_id = models.IntegerField(db_index=True, null=True)
    server_purpose = models.IntegerField(db_index=True, null=True)
    check_update_time = models.DateTimeField(auto_now=True, null=True)
    vm_status = models.IntegerField("虚拟机状态",db_index=True, null=True)
    uuid = models.CharField("虚拟机uuid",max_length=100, db_index=True,null=True)

    def __str__(self):
        return "{} [{}]".format(self.hostname, self.inner_ip)

    class Meta:
        db_table = 'resources_my_server'
        ordering = ['id']


# 业务线表
class Product(models.Model):
    service_name = models.CharField("业务线的名字", max_length=32)
    module_letter = models.CharField("业务线字母简称", max_length=10, db_index=True)
    op_interface = models.CharField("运维对接人", max_length=150)
    dev_interface = models.CharField("业务对接人", max_length=150)
    pid = models.IntegerField("上级业务线id", db_index=True)

    def __str__(self):
        return self.service_name

    class Meta:
        db_table = 'resources_my_product'
        ordering = ['id']