"""Rebuild UK207 MEP start scenario rev02 (MS Project XML) from rev00 .mpp.

Usage: python3 uk207_build_rev02.py <rev00.mpp> <output_dir>
Requires: pip install mpxj JPype1 ; Java 11+.
Applies rev01 fixes, then rev02 changes (critical zone re-quantification,
raft, L1 housekeeping pads, office basement, Option 2 outline fix).
"""
import sys
import jpype, mpxj
jpype.startJVM()
from org.mpxj.reader import UniversalProjectReader
from org.mpxj import Duration, TimeUnit, RelationType, Relation, TaskMode, ConstraintType
from org.mpxj.cpm import MicrosoftScheduler
from org.mpxj.writer import UniversalProjectWriter, FileFormat

NAME='MEP_Start_Scenario_1n2_rev02_20260930'
p=UniversalProjectReader().read(sys.argv[1])
_T={int(t.getID()):t for t in p.getTasks()}
# rev01 fixes
_T[37].setDuration(Duration.getInstance(0,TimeUnit.DAYS)); _T[37].setMilestone(True)
_r=list(_T[5].getPredecessors())[0]; _T[5].getPredecessors().remove(_r); _T[3].getSuccessors().remove(_r)
_T[5].addPredecessor(Relation.Builder().predecessorTask(_T[3]).type(RelationType.START_START).lag(Duration.getInstance(0,TimeUnit.DAYS)))
top=[t for t in p.getTasks() if t.getOutlineLevel() is not None and int(t.getOutlineLevel())==0][0]
o1=[t for t in top.getChildTasks() if str(t.getName())=='Option 1'][0]
o2=[t for t in o1.getChildTasks() if str(t.getName())=='Option 2'][0]
# rev00 outline bug: Option 2 is nested under Option 1 -> outdent to sibling
o1.getChildTasks().remove(o2); o2.setParentTask(top) if hasattr(o2,'setParentTask') else None
top.getChildTasks().add(o2)
def relevel(t,l):
    t.setOutlineLevel(jpype.JInt(l))
    for c in t.getChildTasks(): relevel(c,l+1)
relevel(o2,1)
opts=[o1,o2]
D=lambda n: Duration.getInstance(n,TimeUnit.DAYS)
FS,SS=RelationType.FINISH_START,RelationType.START_START

UID=max(int(t.getUniqueID()) for t in p.getTasks() if t.getUniqueID() is not None)
def link(succ,pred,typ=FS,lag=0):
    succ.addPredecessor(Relation.Builder().predecessorTask(pred).type(typ).lag(D(lag)))
def unlink(succ,pred):
    for r in list(succ.getPredecessors()):
        if r.getPredecessorTask()==pred:
            succ.getPredecessors().remove(r); pred.getSuccessors().remove(r)
def new(parent,name,dur,notes=None,summary=False):
    global UID
    t=parent.addTask(); UID+=1; t.setUniqueID(jpype.JInt(UID)); t.setName(name)
    t.setActualDuration(D(0)); t.setPercentageComplete(jpype.JDouble(0)) if hasattr(t,'setPercentageComplete') else None; t.setTaskMode(TaskMode.AUTO_SCHEDULED)
    t.setConstraintType(ConstraintType.AS_SOON_AS_POSSIBLE)
    if not summary:
        t.setDuration(D(dur)); t.setRemainingDuration(D(dur))
        if dur==0: t.setMilestone(True)
    if notes: t.setNotes(notes)
    return t
def place(parent,task,after):
    ch=parent.getChildTasks(); ch.remove(task); ch.add(ch.indexOf(after)+1,task)

ZONE=('Critical zone (rev02): Phase 1 = Data Hall-3/Data Hall-4 (Level 1). Zone = Substation Phase-1 (DC-L1-44/45, grid 1-2/A-B) '
      '+ north electrical band grid 1-11/A-B + south electrical band grid 2-11/F-G, Ground + Level 1 stacked. Footprint ~1,246 m2/floor, '
      'facade ~1,330 m2 (GF+L1, north+south+west end). Quantities read from RIBA 2 plans 12001/13001/14001; indicative only.')
# quantity-driven durations (workbook rates unchanged; ROUNDUP)
DUR={'Driven pile installation':5,'Pile caps & ground beams: reinforcement fixing':6,'Level 1 slab: soffit formwork strike':8,
     '1.40 m fill':10,'Slab-on-Grade: prep':11,'Blockwork wall':23,'Secondary steel + facade cladding':30}

for opt in opts:
    ch=list(opt.getChildTasks())
    g=lambda s:[t for t in ch if str(t.getName()).startswith(s)][0]
    for k,v in DUR.items():
        for t in ch:
            if str(t.getName()).startswith(k): t.setDuration(D(v)); t.setRemainingDuration(D(v))
    backfill=g('Backfill & compact'); colreb=g('Ground floor RC columns: reinforcement')
    twc=g('Temporary Works Coordinator'); util=g('Utility survey'); piles=g('Driven pile installation')
    l1cure=g('Level 1 slab: cure'); l1strike=g('Level 1 slab: soffit formwork strike')
    mepGF=g('MEP START — Ground Floor'); mepL1=g('MEP START — Level 1'); hkpGF=g('Housekeeping pads')

    # --- raft foundation, critical zone (after backfill, before GF columns)
    r1=new(opt,'Raft foundation, critical zone: blinding & DPM',2)
    r2=new(opt,'Raft foundation, critical zone: reinforcement fixing incl. column starter bars',9,
           'Indicative rate 150 m2/day over ~1,246 m2 (assumption, not a measured rate).')
    r3=new(opt,'Raft foundation, critical zone: edge formwork & stop-ends',3)
    r4=new(opt,'Raft foundation, critical zone: concrete pour (in bays)',2)
    r5=new(opt,'Raft foundation, critical zone: cure (to load columns)',3)
    prev=backfill
    for t in (r1,r2,r3,r4,r5): place(opt,t,prev); prev=t
    link(r1,backfill); link(r2,r1); link(r3,r2,SS,2); link(r4,r2); link(r4,r3); link(r5,r4)
    unlink(colreb,backfill); link(colreb,r5)

    # --- Level 1 equipment bases (Phase 1 sits on L1)
    hkpL1=new(opt,'Housekeeping pads/plinths, Level 1 equipment bases (Substation Phase-1 / RMU / TX / Electrical Rooms)',4)
    place(opt,hkpL1,hkpGF); link(hkpL1,l1cure); link(mepL1,hkpL1)

    # --- office basement (grid 11-13 / C'-G, outside critical zone, parallel)
    bs=new(opt,'Office basement (grid 11-13 / C\'-G, -4.00 m) — outside critical zone, parallel',0,
           'Basement per UK207-100-A1-AP00-12001: fire pump room, 2x water tanks, public health room, stairs, goods lift (~450 m2). '
           'Indicative durations; not on the critical zone MEP path. Shared crane/concrete gangs not resource-levelled.',summary=True)
    place(opt,bs,mepL1)
    B=[('Basement: excavation support installation (per TW design)',5),
       ('Basement: bulk excavation to formation level',5),
       ('Basement: driven piles',2),
       ('Basement: pile testing & cut-down',2),
       ('Basement: blinding',1),
       ('Basement: below-ground waterproofing to raft (BS 8102)',3),
       ('Basement raft: reinforcement fixing incl. wall starters',4),
       ('Basement raft: concrete pour',1),
       ('Basement raft: cure',3),
       ('Basement retaining walls: reinforcement & formwork',8),
       ('Basement retaining walls: concrete pour',1),
       ('Basement retaining walls: cure & strike',3),
       ('Basement: external waterproofing to walls & backfill',4),
       ('Ground floor slab over basement: falsework, formwork & reinforcement',6),
       ('Ground floor slab over basement: concrete pour',1),
       ('Ground floor slab over basement: cure',7)]
    bt=[new(bs,n,d) for n,d in B]
    link(bt[0],util); link(bt[0],twc); link(bt[1],bt[0]); link(bt[2],bt[1]); link(bt[2],piles)
    link(bt[3],bt[2],FS,1)
    for i in range(4,16): link(bt[i],bt[i-1])

    for t in (mepGF,mepL1): t.setNotes(ZONE)
    mepL1.setName('MEP START — Level 1 (Phase 1: Substation Phase-1 + DH-3/DH-4 electrical bands)')
    mepGF.setName('MEP START — Ground Floor (bands below Phase 1 zone; serve DH-1/DH-2)')

p.getTasks().synchronizeTaskIDToHierarchy()
p.getTasks().updateStructure() if hasattr(p.getTasks(),'updateStructure') else None
top.setName(NAME); p.getProjectProperties().setName(NAME)
MicrosoftScheduler().schedule(p,p.getProjectProperties().getStartDate())
UniversalProjectWriter(FileFormat.MSPDI).write(p,f'{sys.argv[2]}/{NAME}.xml')
def walk(t):
    yield t
    for c in t.getChildTasks(): yield from walk(c)
for t in walk(top):
    pr=",".join(f"{r.getPredecessorTask().getID()}{'SS' if r.getType()==SS else 'FS'}{'' if r.getLag().getDuration()==0 else '+'+str(r.getLag())}" for r in t.getPredecessors())
    print(f"{t.getID()}\t{'  '*int(t.getOutlineLevel())}{str(t.getName())[:70]}\t{t.getDuration()}\t{str(t.getStart())[:10]}\t{str(t.getFinish())[:10]}\t{'C' if t.getCritical() else ''}\t{pr}")
