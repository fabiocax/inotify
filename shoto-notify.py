import inotify.adapters
import subprocess
import threading
import yaml
import fire

def exec_cmd(*args):
        isshell=False
        p = subprocess.Popen(args,stdout = subprocess.PIPE,stderr =subprocess.PIPE,shell=isshell)
        saida=p.wait()
        stdout, stderr= p.communicate()
        return (p.pid,saida,stdout,stderr)


class Monitory:
    def __init__(self):
        pass    
    def events(self,event,yamlconf):
        try:
            self.cmds=yamlconf['monitor']['commands']
        except:
            self.cmds=[]
        self.event=event    


        self.dir=self.event[2]+'/'+self.event[3]    
        if self.event[1][0]=="IN_OPEN":
            self.IN_OPEN()
        elif self.event[1][0]=="IN_ATTRIB":
            self.IN_ATTRIB()        
        elif self.event[1][0]=="IN_CLOSE_WRITE":
            self.IN_CLOSE_WRITE()
        elif self.event[1][0]=="IN_DELETE":
            self.IN_DELETE()
        elif self.event[1][0]=="IN_MODIFY":
            self.IN_MODIFY()        
        elif self.event[1][0]=="IN_ACCESS":
            self.IN_ACCESS()              
        
    def IN_OPEN(self):
        for cmdl in self.cmds:
            e=exec_cmd(cmdl,self.dir)
            print('CMD:','OPEN',cmdl,self.dir,e)
        
    def IN_ATTRIB(self):
        for cmdl in self.cmds:
            e=exec_cmd(cmdl,self.dir)
            print('CMD:','IN_ATTRIB',cmdl,self.dir,e)
        
    def IN_CLOSE_WRITE(self):
        for cmdl in self.cmds:
            e=exec_cmd(cmdl,self.dir)   
            print('CMD:','IN_CLOSE_WRITE',cmdl,self.dir,e)

    def IN_DELETE(self):
        for cmdl in self.cmds:
            e=exec_cmd(cmdl,self.dir)       
            print('CMD:','IN_DELETE',cmdl,self.dir,e)

    def IN_MODIFY(self):
        for cmdl in self.cmds:
            e=exec_cmd(cmdl,self.dir)
            print('CMD:','IN_MODIFY',cmdl,self.dir,e)
    def IN_ACCESS(self):
        for cmdl in self.cmds:
            e=exec_cmd(cmdl,self.dir)
            print('CMD:','IN_ACCESS',cmdl,self.dir,e)    
        
def parallel_mon(line):
    print('Monitoring:',line['monitor']['patch'],'('+line['monitor']['event']+')') 

    patch=line['monitor']['patch']

    try:
        exclude_files=line['monitor']['exclude'].split(',')
    except:
        exclude_files=[]

    check_events=line['monitor']['event']
    include_dir=False
    
    i = inotify.adapters.InotifyTree(patch)
    moni=Monitory()        
    for event in i.event_gen(yield_nones=False):
        if event[1][0] in check_events:
            if not 'IN_ISDIR' in event[1] or include_dir == False:
                if not event[3] in exclude_files :
                    moni.events(event,line)

class Execs():
    def __init__(self,conf='conf.yaml'):
        self.config = conf

    def exec(self):
        with open(self.config) as f:    
            self.data = yaml.load(f, Loader=yaml.FullLoader)
        for line in  self.data:
            t = threading.Thread(target=parallel_mon,args=(line,))
            t.start()
                   
        return ''

def _main():
    fire.Fire(Execs)

if __name__ == '__main__':
    _main()