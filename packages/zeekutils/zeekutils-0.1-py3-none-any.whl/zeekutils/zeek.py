import  subprocess

class ZeekNodes:
    def __init__(self,path):
        self.path = path
        self.logger = 0
        self.manager = 0
        self.proxy = 0
        self.workers = 0
        self.status = self.getstatus()

    def start(self):
        pi = subprocess.Popen('%s/zeekctl start' % self.path, shell=True, stdout=subprocess.PIPE)
        result = pi.stdout.read()
        print(result)
        return True

    def stop(self):
        pi = subprocess.Popen('%s/zeekctl stop' % self.path, shell=True, stdout=subprocess.PIPE)
        result = pi.stdout.read()
        print(result)
        return True

    def restart(self):
        pi = subprocess.Popen('%s/zeekctl restart' % self.path, shell=True, stdout=subprocess.PIPE)
        result = pi.stdout.read()
        print(result)
        return True

    def deploy(self):
        pi = subprocess.Popen('%s/zeekctl deploy' % self.path, shell=True, stdout=subprocess.PIPE)
        result = pi.stdout.read()
        print(result)
        return True

    def getstatus(self):
        status = True
        pi = subprocess.Popen('%s/zeekctl status' % self.path, shell=True, stdout=subprocess.PIPE)
        result = pi.stdout.read()
        nodes = result.split('\n')
        del nodes[0]
        del nodes[-1]
        for node in nodes:
            if 'running' not in node:
                status = False
        return status

    def updateRule(self):
        '''从服务端下载全量文件至当前NIDS系统'''
        return True

    def getversion(self):
        return "3.1.3"

