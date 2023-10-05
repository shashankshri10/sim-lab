class lcg:
    def __init__(self,*args): # args -> seed,a,c,m,n=1 (Def.)
        # args when single num -> seed,a,c,m
        # args when num, defined -> seed,a,c,m,num
        self.state = args[0]
        self.a = args[1]
        self.c = args[2]
        self.m = args[3]
        self.rtype = "num"
        if (len(args)==5):
            self.num = args[4]
            self.rtype = "list"
    # generates either a num or a list of random no.s
    def gen(self):
        res = []
        if (self.rtype == "num"):
            self.state = (self.a*self.state+self.c)%self.m
            res = self.state/(self.m+1)
        else:
            for i in range(0,self.num):
                self.state = (self.a*self.state+self.c)%self.m
                res.append(self.state/(self.m+1))
        return res