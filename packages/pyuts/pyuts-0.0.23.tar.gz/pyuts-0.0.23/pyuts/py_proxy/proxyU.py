# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
try:
    from ..py_crawl.httpU import HttpU
except ImportError as e:
    print(e)
try:
    from .proxyCrawlerU import ProxyCrawlerU
except ImportError as e:
    print(e)
try:
    from ..py_mix.ctrlCU import CtrlCU
except ImportError as e:
    print(e)
try:
    from ..py_mix.asyncU import AsyncU
except ImportError as e:
    print(e)
try:
    from ..py_file.fileU import FileU
except ImportError as e:
    print(e)
try:
    from ..py_db.redisDBU import RedisDBU
except ImportError as e:
    print(e)
try:
    from ..py_db.mongoDBU import MongoDBU
except ImportError as e:
    print(e)
import time
CHECK_BAIDU = "https://www.baidu.com"
DBName = "proxy"
CHECKED_TBNAME = "checked"

class ProxyU(PyApiB):
    """
    代理相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def __init__(self):
        self.redis = RedisDBU()
        self.mongoDB = MongoDBU()
        self.redisPreKey = "proxyU"
        self.ctrlCU = None
        
    def addProxyCrawlers(self, crawlers):
        from ..py_mix.moduleU import ModuleU
        cs = ModuleU().importClsByPcls(crawlers,ProxyCrawlerU)
        for c in cs:
            crawlerName = c
            if "." in c:
                crawlerName = c.split(".")[-1]
            self.addProxyCrawler(crawlerName, cs[c])
    
    def addProxyCrawler(self,crawlerName:str, crawler:ProxyCrawlerU):
        print(f"addProxyCrawler {crawlerName}:{crawler}")
        proxy_crawlers = getattr(self,'proxy_crawlers',{})
        proxy_crawlers[crawlerName] = crawler
        setattr(self,'proxy_crawlers',proxy_crawlers)
        
    def getProxyMeta(self,ipSign=None):
        """ 获取一个代理 """
        ipSignKey = None if not ipSign else f"{self.redisPreKey}:ipSign:{ipSign}"
        key = f"{self.redisPreKey}:checked"
        if ipSignKey:
            cacheMeta = self.redis.get(ipSignKey)
            if cacheMeta:
                return cacheMeta
        metas = self.redis.srandmember(key)
        if metas and len(metas)>0:
            meta = metas[0]
            if ipSignKey:
                self.redis.set(ipSignKey,meta,ex=self.getExByIpsign(ipSign))
            return meta
        return None
    
    def produceIpSign(self,ex=600):
        """ 生成一个ip标记，如果传入ipSign一样，会尽量返回同一个代理，ex秒后过期 """
        return self.redis.randomkey()+str(ex).zfill(5)
    
    def getExByIpsign(self, ipSign):
        return int(ipSign[-5:])
    
    def proxyToMeta(self, proxy, ipSign=None):
        """ dict的代理转meta格式 """
        if proxy.get("host") == "proxyU":
            return self.getProxyMeta(ipSign)
        if proxy.get("user") and proxy.get("host") and proxy.get("port"):
            meta = f"http://{proxy.get('user')}:{proxy.get('pswd')}@{proxy.get('host')}:{proxy.get('port')}"
        elif proxy.get("host") and proxy.get("port"):
            meta = f"http://{proxy.get('host')}:{proxy.get('port')}"
        return meta
    
    def metaToProxy(self, meta):
        """ meta格式转dict代理 """
        if "//" in meta:
            pInfo = meta.split("//")[1]
            user,pswd = "",""
            if "@" in pInfo:
                up, pInfo = pInfo.split("@")
                if ":" in up:
                    user,pswd = up.split(":")
                else:
                    user = up
            if ":" in pInfo:
                host, port = pInfo.split(":")
                return {"host":host,"port":port,"user":user,"pswd":pswd}
        return {}
        
    def __readLocalMetas(self, type="source", maxLen=1000):
        key = f"{self.redisPreKey}:{type}"
        return self.redis.get_str_list(key)
        
    def __saveLocalMetas(self, metas, type="source", maxLen=1000):
        key = f"{self.redisPreKey}:{type}"
        self.redis.set_str_list(key, metas[-maxLen:])
        
    def __pushLocalMetas(self, metas, type="source", maxLen=1000):
        key = f"{self.redisPreKey}:{type}"
        self.redis.rpush_str(key,metas,maxLen)
        
    def __isMetaSame(self, meta1, meta2):
        m1,m2 = meta1,meta2
        if isinstance(meta1,dict):
            m1 = meta1.get('meta')
        if isinstance(meta2,dict):
            m2 = meta2.get('meta')
        return m1 == m2
    
    def __isInMetas(self, meta1, metas):
        return any(list(map(lambda x: self.__isMetaSame(meta1, x),metas)))
        
    def __upsertCheckedMeta(self, meta, maxLen=1000):
        """ 更新有效的代理入mongoDB,并同步一份至redis """
        key = f"{self.redisPreKey}:checked"
        if self.mongoDB.hasInit():
            self.mongoDB.upsert_one(DBName,CHECKED_TBNAME,{"meta":meta.get("meta")},meta)
        self.redis.sadd(key,meta.get("meta"))
        
    def __removeCheckedMeta(self, metaStr):
        """ 删除无效的代理mongoDB和redis """
        if self.mongoDB.hasInit():
            self.mongoDB.delete_many(DBName,CHECKED_TBNAME,{"meta":metaStr})
        self.__removeCheckedFromRedis(metaStr)
        
    def __removeCheckedFromRedis(self, *metaStrs):
        """ 从redis的checked中删除一个代理 """
        key = f"{self.redisPreKey}:checked"
        self.redis.srem(key,*metaStrs)
        
    def __filtHasChecked(self, proxys):
        key = f"{self.redisPreKey}:checked"
        ms = self.redis.srandmember(key)
        newProxys = []
        for proxy in proxys:
            meta = f"http://{proxy.get('user')}:{proxy.get('pswd')}@{proxy.get('host')}:{proxy.get('port')}"
            if meta not in ms:
                newProxys.append(proxy)
        return newProxys
        
    def __popLocalMeta(self, type="source"):
        key = f"{self.redisPreKey}:{type}"
        return self.redis.lpop_str(key)
        
    def __saveToWaitCheck(self, proxys):
        # 将没有在等待队列中的元素搬到等待队列
        waitCheckMetas = self.__readLocalMetas("waitCheck")
        needPushs = []
        for proxy in proxys:
            meta = ""
            if isinstance(proxy,str):
                meta = proxy
            else:
                meta = self.proxyToMeta(proxy)
            if not self.__isInMetas(meta, waitCheckMetas):
                needPushs.append(meta)
        if needPushs:
            print(f"tranProxys:{len(needPushs)}")
            self.__pushLocalMetas(needPushs, "waitCheck")
            
    def __popWaitCheck(self):
        return self.__popLocalMeta("waitCheck")
        
    def crawlProxyAndSave(self, crawlerName):
        """ 采集名称为crawlerName的爬虫，并保存所获得的代理 """
        proxy_crawlers = getattr(self,'proxy_crawlers',{})
        crawler = proxy_crawlers.get(crawlerName)
        if crawler and crawler.crawlerEnable:
            proxys = crawler().getProxys()
            print(f"crawlProxyAndSave:{len(proxys)}")
            proxys = self.__filtHasChecked(proxys)
            self.__saveToWaitCheck(proxys)
        
    def crawlProxysAndSave(self):
        """ 采集所有爬虫，并保存所获得的代理 """
        asyncU:AsyncU = AsyncU.produce("ProxyU")
        runKeys = asyncU.getRunningKeys()
        proxy_crawlers = getattr(self,'proxy_crawlers',{})
        for k in proxy_crawlers:
            if k not in runKeys:
                asyncU.asyncRun(target=self.crawlProxyAndSave,args=(k,), asyncKey=k, isProcess=False)
    
    def loopCrawl(self, crawlDuring):
        """ 循环采集所有爬虫，并保存所获得的代理 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        ctrlCU.on()
        while not ctrlCU.isExit():
            wkey = ctrlCU.wantSleep()
            self.crawlProxysAndSave()
            ctrlCU.toSleep(crawlDuring,wkey)
        
    def checkOneProxy(self, proxyMeta=None, timeout=60, checkUrl=CHECK_BAIDU):
        """ 检测一次代理的可用性，并保存入checked。proxyMeta如果为空，则从等待队列中pop一个代理 """
        if proxyMeta == None:
            proxyMeta = self.__popWaitCheck()
        # print(f"check {proxyMeta}")
        if proxyMeta:
            res = HttpU().get(checkUrl,proxyMeta=proxyMeta,timeout=timeout)
            if str(res.get('code')) == "200":
                meta = {"meta":proxyMeta,"ut":time.time()}
                print(f"check {proxyMeta} Pass!!")
                self.__upsertCheckedMeta(meta)
            else:
                print(f"check {proxyMeta} NoPass!!")
                self.__removeCheckedMeta(proxyMeta)
            return True
        else:
            return False
                
    def loopCheckOneProxy(self, timeout=20, checkUrl=CHECK_BAIDU):
        """ 一个线程循环检测等待队列中代理的可用性，并保存入checked。 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        while not ctrlCU.isExit():
            res = False
            try:
                res = self.checkOneProxy(timeout=timeout,checkUrl=checkUrl)
            except Exception as e:
                print("checkOneProxy Failed!!!")
            if not res:
                time.sleep(5)
            else:
                time.sleep(1)
            
    def tranExpire(self, expireTime=600):
        """ 转移过期的入待查队列 """
        if self.mongoDB.hasInit():
            nowTime = time.time()
            needChecks = self.mongoDB.find(DBName,CHECKED_TBNAME,{"ut":{"$lte":(nowTime-expireTime)}})
            if needChecks:
                metas = list(map(lambda x: x.get("meta"),needChecks))
                self.__saveToWaitCheck(metas)
        else:
            needChecks = self.__getCheckedList()
            if needChecks:
                self.__saveToWaitCheck(needChecks)
            
    def __getCheckedList(self):
        key = f"{self.redisPreKey}:checked"
        checkeds = []
        try:
            checkedset = self.redis.srandmember(key,number=500)
            checkeds = list(checkedset)
        except Exception as identifier:
            pass
        return checkeds
        
    def loopTranExpire(self,expireTime=600):
        """ 定时转移过期的入待查队列 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        while not ctrlCU.isExit():
            time.sleep(60)
            self.tranExpire(expireTime)
        
    def loopCheck(self,checkUrl=CHECK_BAIDU,checkTimeout=20,checkThreadNum=16,expireTime=600):
        """ 多线程循环检测等待队列中代理的可用性，并保存入checked。 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        ctrlCU.on()
        asyncU:AsyncU = AsyncU.produce("ProxyU")
        asyncU.asyncRun(target=self.loopTranExpire, args=(expireTime,), asyncKey="loopTranExpire", isProcess=False)
        for c in range(checkThreadNum):
            asyncU.asyncRun(target=self.loopCheckOneProxy,args=(checkTimeout,checkUrl,), asyncKey=f"loopChechProxys_{c}", isProcess=False)
        
    def loopCrawlAndCheck(self,crawlDuring=20,checkUrl=CHECK_BAIDU,checkTimeout=20,checkThreadNum=16,expireTime=600):
        """ 总入口，启动所有采集和检测进程 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        ctrlCU.on()
        self.loopCheck(checkUrl=checkUrl, checkTimeout=checkTimeout,checkThreadNum=checkThreadNum,expireTime=expireTime)
        self.loopCrawl(crawlDuring)
        
    def startServer(self, port=8080):
        """ 开始总代理服务
        pip install pyopenssl
        pip install tornado
        pip install pycurl
        """
        from ..py_server.serverU import ServerU
        # from .proxyHandler import ProxyHandler
        # ServerU().http(port).addHandler(ProxyHandler).start()
        