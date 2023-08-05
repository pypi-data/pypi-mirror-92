class armstrong:
    def A_strong(num):
        s=0
        k=num
        while k>0:
            r=k%10
            s+=(r**3)
            k//=10
        if s==num:
            return True
        else:
            return False
