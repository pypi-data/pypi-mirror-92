# coding=utf-8
import subprocess
import shutil
import os
import time
import shlex


class ZeekNodes:
    def __init__(self, path):
        self.basepath = shlex.quote(path)
        self.zeekpolicypath = self.basepath + "/share/zeek/site/"
        self.zeekctlpath = self.basepath + "/bin/zeekctl"
        self.zeekpath = self.basepath + "/bin/zeek"
        self.tmprulefilepath = self.basepath + "/tmprulefile/"
        self.pcapfilepath = self.basepath + "/pcapfile/"
        self.backuptmprulefilepath = self.basepath + "/tmprulefile/backuprule/"
        self.ruleloaderpath = self.basepath + "/share/zeek/site/rule_loader.zeek"

    def start(self):
        pi = subprocess.Popen('%s start' % self.zeekctlpath, shell=True, stdout=subprocess.PIPE)
        result = str( pi.stdout.read(), encoding="utf-8")
        return {"result": "success", "log": result}

    def stop(self):
        pi = subprocess.Popen('%s stop' % self.zeekctlpath, shell=True, stdout=subprocess.PIPE)
        result = str( pi.stdout.read(), encoding="utf-8")
        return {"result": "success", "log": result}

    def restart(self):
        pi = subprocess.Popen('%s restart' % self.zeekctlpath, shell=True, stdout=subprocess.PIPE)
        result = str(pi.stdout.read(), encoding="utf-8")
        return {"result": "success", "log": result}

    def deploy(self):
        pi = subprocess.Popen('%s deploy' % self.zeekctlpath, shell=True, stdout=subprocess.PIPE)
        result = str( pi.stdout.read(), encoding="utf-8")
        return {"result": "success", "log": result}

    def getstatus(self):
        status = "up"
        pi = subprocess.Popen('%s status' % self.zeekctlpath, shell=True, stdout=subprocess.PIPE)
        result = str( pi.stdout.read(), encoding="utf-8")
        nodes = result.split('\n')
        del nodes[0]
        del nodes[-1]
        for node in nodes:
            if 'running' not in node:
                status = "down"
        return {"status": status, "log": result}

    def updaterule(self):
        """从服务端下载全量文件至当前NIDS系统"""
        return True

    def cprulefile(self,rulename):
        if os.path.exists(self.zeekpolicypath + rulename):
            shutil.rmtree(self.zeekpolicypath + rulename)
        shutil.copytree(self.tmprulefilepath + rulename,self.zeekpolicypath + rulename)

    def getversion(self):
        pi = subprocess.Popen('%s -v' % self.zeekpath, shell=True, stdout=subprocess.PIPE)
        result = str( pi.stdout.read(), encoding="utf-8")
        version = result.strip().split(' ')[-1]
        return {"version": version, "log": result}

    def getrule(self):
        rules = []
        with open("%s" % self.ruleloaderpath) as f:
            for rule in f.readlines():
                rules.append(rule.strip().replace('@load ', ''))
            return {"result": "success", "rules": rules}

    def addrules(self, rule):

        existrules = self.getrule().get('rules')
        with open("%s" % self.ruleloaderpath, "w") as f:
            f.truncate()
            if isinstance(rule, list):
                for _ in rule:
                    self.cprulefile(_)
                existrules = existrules + rule
            else:
                existrules.append(rule)
                self.cprulefile(rule)
            rules = list(set(existrules))
            for _ in rules:
                if (_ is not None) and (_.strip() != ""):
                    f.write("@load " + _ + '\n')

    def delrules(self, rule):
        existrules = self.getrule().get('rules')
        with open("%s" % self.ruleloaderpath, "w") as f:
            f.truncate()
            if isinstance(rule, list):
                existrules = list(set(existrules) - set(rule))
            else:
                if rule in existrules:
                    existrules.remove(rule)
            rules = list(set(existrules))
            for _ in rules:
                if (_ is not None) and (_.strip() != ""):
                    f.write("@load " + _ + '\n')

    def generzeekfile(self, ruleinfo):
        rulepath = self.tmprulefilepath + ruleinfo.get('rulename')
        timestamp = str(int(time.time()))
        backuprulepath = self.backuptmprulefilepath + ruleinfo.get('rulename') + timestamp
        if not os.path.exists(self.tmprulefilepath):
            os.mkdir(self.tmprulefilepath)
        if not os.path.exists(self.backuptmprulefilepath):
            os.mkdir(self.backuptmprulefilepath)
        if os.path.exists(rulepath):
            shutil.move(rulepath, backuprulepath)
        os.mkdir(rulepath)
        with open(rulepath + "/__load__.zeek", "w") as f:
            f.write(ruleinfo.get('zeekruletext'))
        with open(rulepath + "/%s.sig" % ruleinfo.get('rulename'), "w") as f:
            f.write(ruleinfo.get('sigruletext'))

    def testrule(self, ruleinfo, pcapfile):
        """/data/zeek/bin/zeek -r 210122-1Sd7_G0cCkVK2oUk9x0zLsRr.pcap  __load__.zeek """
        self.generzeekfile(ruleinfo)
        pcapfilepath = self.pcapfilepath + pcapfile
        rulepath = self.tmprulefilepath + ruleinfo.get('rulename')
        noticefile = rulepath + '/notice.log'
        if not os.path.exists(self.pcapfilepath):
            os.mkdir(self.pcapfilepath)
        pi = subprocess.Popen('cd %s && /data/zeek/bin/zeek -r %s  __load__.zeek ' % (shlex.quote(rulepath), shlex.quote(pcapfilepath)), shell=True, stdout=subprocess.PIPE)
        result = str( pi.stdout.read(), encoding="utf-8")
        if  os.path.exists(noticefile):
            with open(noticefile) as f:
                return {"result":"success","log": result,"notice": f.read()}
        else:
            return {"result": "fail", "log": result, "notice": ""}
