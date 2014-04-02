
start = "B.C.D.F.G.H.J.L.M.N.P.R.S.T.V.Qu.Ch.St"
start = start.split('.')
then = "a.e.i.o.u.on.ou.ai.en.in"
then = then.split('.')

allU = []
allL = []

for f in start:
    for t in then:
        allU.append((f+t))
        allL.append((f+t).lower())
        
    