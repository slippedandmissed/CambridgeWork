#!/usr/bin/python3.11
import numpy as np

# Slightly simplified implementation
#   Jiggled indices to better fit zero-indexed arrays etc.

def fpbisp(tx, ty, c, kx, ky, x, y):
    nx = len(tx)
    ny = len(ty)
    mx = len(x)
    my = len(y)
    lx = np.empty((mx,), dtype=int)
    ly = np.empty((my,), dtype=int)
    z = np.empty((mx*my,))
    wx = np.empty((mx,kx+1))
    wy = np.empty((my,ky+1))

    tb = tx[kx]
    te = tx[nx - kx - 1]
    l = kx+1

    for i in range(mx):
        arg = max(tb, min(te, x[i]))
        while arg >= tx[l] and l < nx - kx - 1:
            l += 1
        
        print(l)

        h = fpbspl(tx, kx, arg, l)

        lx[i] = l-kx-1
        
        for j in range(kx+1):
            wx[i, j] = h[j]

    tb = ty[ky]
    te = ty[ny-ky-1]
    l = ky + 1

    for i in range(my):
        arg = max(tb, min(te, y[i]))
        while arg >= ty[l] and l < ny-ky - 1:
            l += 1

        h = fpbspl(ty, ky, arg, l)

        ly[i] = l-ky-1
        for j in range(ky + 1):
            wy[i, j] = h[j]

    m = 0
    for i in range(mx):
        l = lx[i]*(ny-ky-1)
        for i1 in range(kx+1):
            h[i1] = wx[i, i1]
        for j in range(my):
            l1 = l+ly[j] - 1
            sp = 0
            for i1 in range(kx+1):
                l2 = l1
                for j1 in range(ky + 1):
                    l2 += 1
                    sp = sp+c[l2]*h[i1]*wy[j, j1]
                l1 += ny-ky-1
            z[m] = sp
            m += 1

    return z.reshape((mx,my))


def fpbspl(t, k, x, l):
    n = len(t)
    h = np.empty((k+1,))
    hh = np.empty((k,))

    h[0] = 1
    for j in range(k):
        for i in range(j+1):
            hh[i] = h[i]
        h[0] = 0
        for i in range(j+1):
            li = l+i
            lj = li-j-1
            if t[li] != t[lj]:
                f = hh[i]/(t[li]-t[lj])
                h[i] = h[i]+f*(t[li]-x)
                h[i+1] = f*(x-t[lj])
            else:
                h[i+1] = 0
    return h


if __name__ == "__main__":
    import scipy.interpolate

    tx = np.array([0.0, 0.0, 0.0, 0.0, 0.032612818114835115, 0.07213587288641929, 0.10317611363419149, 0.13070498805670921, 0.1587536709392709, 0.1835120919056885, 0.2086351863548237, 0.23972366620527402, 0.27573451807881305, 0.30910841234361297, 0.33555164785656527, 0.36519021120799033, 0.38664092527907534, 0.40405063788316836, 0.4358512451659136, 0.4648022602467377,
                  0.48895136297607394, 0.5166474253926234, 0.5451617073329268, 0.570474374934004, 0.5957104327517436, 0.6266960064519695, 0.655517521935678, 0.6870069476445619, 0.720492882628007, 0.7394770520424997, 0.7574425303337562, 0.7935444463588542, 0.8263372927259149, 0.8621776108086563, 0.8812212003342275, 0.9006096343920076, 0.9376544305463147, 0.9720662974887547, 1.0, 1.0, 1.0, 1.0])
    ty = np.array([0.0, 0.0, 0.0, 0.0, 0.023627651936890537, 0.06153058804514242, 0.09582891652240484, 0.12698822868589552, 0.16000104011346994, 0.19186983065459862, 0.21926101330606743, 0.2370607295082237, 0.25476453174939684, 0.29327419892181933, 0.32649739386124105, 0.35869429931432606, 0.381982513402981, 0.411347082512085, 0.4396944305513502, 0.471014426083932,
                  0.5058423982499511, 0.5416428123797922, 0.5619402303988588, 0.5811292888278793, 0.608703226893385, 0.6349200841494712, 0.6561774680511215, 0.6814735767411423, 0.7145977500573716, 0.7464098626044485, 0.772315397210871, 0.7999727957644405, 0.8255998215746172, 0.8519512831582456, 0.8871188939039152, 0.9073152942931672, 0.9288932327949542, 0.9666017780988633, 1.0, 1.0, 1.0, 1.0])
    c = np.array([0.5005750798633244, 0.5268311559277584, 0.5913916171592807, 0.7836896135260898, 0.8344863336969138, 0.5910777412845959, 0.33279378388655334, 0.36001130639900414, 0.4626401464932401, 0.48724576676520553, 0.45732891819533916, 0.4469927081373378, 0.6995185927132028, 0.7879269145627188, 0.7762111467708387, 0.7549255301589098, 0.6708660038222222, 0.47646212994381143, 0.2545493449760533, 0.2602032492801147, 0.35937721639326653, 0.44553218024259206, 0.5267332678257507, 0.6194919842762663, 0.7338531115584536, 0.8293210850130245, 0.7836670737383565, 0.5702091760981737, 0.3674103023657251, 0.380952725087648, 0.576941046595526, 0.7398290674629793, 0.7359537250037672, 0.7124648235245017, 0.721410224262336, 0.7503757831212583, 0.6790438181881248, 0.6398629763918205, 0.5404894808844319, 0.5661642469058324, 0.6220644346126727, 0.8107665796739295, 0.8281726944006069, 0.5660629250724281, 0.25191188356436, 0.2581855041549542, 0.40551162643748884, 0.47164784358464734, 0.47798965587135606, 0.5092878249582539, 0.7742601208894846, 0.8704638738304404, 0.8204664904826564, 0.7637559194177145, 0.6357720737236915, 0.4252102140808614, 0.2329351416977238, 0.2916733488519521, 0.43453489597426515, 0.5501055224112353, 0.6333485316192878, 0.7189910610941008, 0.8415807403265549, 0.9157850301715156, 0.813963600699311, 0.5477698881849213, 0.2920421148718538, 0.28993028169253926, 0.49845454998461275, 0.684153333669774, 0.6634588804948534, 0.6335751465973901, 0.6446556248559298, 0.688655069382012, 0.6399413599469762, 0.5999541506286239, 0.6386998688927489, 0.6633781585208778, 0.697296680516374, 0.8337826791310338, 0.7662101534746169, 0.4629762966974774, 0.12138765724015933, 0.07746973647383666, 0.26425580628736817, 0.4076153568656473, 0.5045576044531438, 0.6001001617573087, 0.8289525479165116, 0.9231218469494259, 0.8207675319272404, 0.6771974109693765, 0.47293760515987515, 0.25312965024192735, 0.11664821845655762, 0.30560186899726655, 0.5796978960626216, 0.7909680128191412, 0.8880746567200528, 0.8900896787424925, 0.9497614902639289, 0.9694405293600025, 0.8099665280726361, 0.4840020033164926, 0.161127284932272, 0.10144873193436493, 0.309548498860793, 0.5616028314266939, 0.6112089433330908, 0.573516665134809, 0.5545946450858114, 0.6601306697180378, 0.68236876709186, 0.6507214176421707, 0.3571369756108677, 0.3858733732332832, 0.3880556727138225, 0.4894000570388103, 0.5719882146169131, 0.3559149053735735, 0.1203334548794286, 0.19964254790893904, 0.4010919736287353, 0.5081465093073001, 0.5673289771055363, 0.6272270735492034, 0.6461207096976912, 0.6349361035347151, 0.5642908613702436, 0.4941653093416196, 0.41865122148071965, 0.29751987663997503, 0.13103274937259493, 0.2011570827864128, 0.3590009139173233, 0.49490381398461253, 0.5597592255079477, 0.5227509518761018, 0.5490340575847804, 0.6086270578723718, 0.5712417721516821, 0.36546764067206566, 0.21689742854971783, 0.20578031522736584, 0.3075348313605492, 0.3985790174746049, 0.4620342381232959, 0.5484220006345747, 0.6657015486050015, 0.7873618936137149, 0.797099725406083, 0.8023548659745808, 0.06198532447364724, 0.08647378163233536, 0.10196409111095263, 0.31687285082589356, 0.5856779451296203, 0.49350042882318396, 0.30105197486758956, 0.33343112250717866, 0.47183716371614387, 0.5464812641698962, 0.5969913650456207, 0.627546048030162, 0.5036845508051458, 0.37765918476278454, 0.34386793626295964, 0.4075143697865561, 0.5814331521787783, 0.6512386862631732, 0.4988643812243841, 0.37097296783440137, 0.2859040430450777, 0.26277741469838933, 0.29749854434007866, 0.3421701961685845, 0.38798019927030525, 0.41975343007536214, 0.3452814305023251, 0.29668863082850855, 0.3823984489757341, 0.40487939609527734, 0.2914256673767186, 0.14285192068263533, 0.16209120901269944, 0.3370252019370985, 0.602981183721841, 0.8067729979237174, 0.7652142699506779, 0.7589859080580457, 0.11548831398373566, 0.12400482398825267, 0.14019037034083257, 0.38469494142886734, 0.7010195133483884, 0.7192544039463508, 0.5087753006877258, 0.37349000064492854, 0.4256919117132637, 0.5322680265771239, 0.6594447612660694, 0.7211192493778518, 0.5357945169582664, 0.340632029245843, 0.27309210472863416, 0.3491357562389357, 0.6174812513123703, 0.8336635450856436, 0.8019258387812488, 0.6229190336916666, 0.4838408233460967, 0.4281992090392612, 0.483253757839572, 0.5929050848914073, 0.6007268685656649, 0.4777405197704259, 0.2924885756039915, 0.3412438864030664, 0.5261414984486149, 0.5967109010254682, 0.45026005991410106, 0.2407092437144112, 0.19549547188346644, 0.3040736461969902, 0.560392930994943, 0.8343670925772522, 0.7459753893306486, 0.6967383512819428, 0.24949915777860956, 0.26374438133025024, 0.2865275086930903, 0.44154058276324215, 0.7664077374306492, 0.8344697556734859, 0.6252763514426509, 0.4245254695294405, 0.46458683568091436, 0.5843263930517548, 0.7299647028160217, 0.8001180162635654, 0.6890986451012044, 0.49800463845229503, 0.3723757446072754, 0.3481557698212868, 0.4869598836751677, 0.7628052599975601, 0.9325543382148571, 0.7972836352177719, 0.6867570704420728, 0.6422516687954143, 0.6826309719306386, 0.7709872682782769, 0.7518029829759885, 0.583780834764198, 0.3743547131161268, 0.4416378984056217, 0.6522485144178787, 0.7749660859127863, 0.7271604785740468, 0.5681602945382326, 0.4535102080988398, 0.4761390518315517, 0.6561536088732585, 0.8745314011788892, 0.7182250069030701, 0.6322149164439963, 0.26010958285009184, 0.28720851530584973, 0.3422457469287327, 0.38848300259056806, 0.6680339324559496, 0.7939622774438612, 0.6608704560080142, 0.5198130685432313, 0.5551147881536077, 0.6498258964307878, 0.7731392777227312, 0.8288694657943232, 0.7787091850187647, 0.631234300400117, 0.49749775859237966, 0.38833157258805856, 0.3638892673711624, 0.6065800948756006, 0.9005743875534002, 0.8706490960225238, 0.8134778322386147, 0.7886054192344338, 0.7643762978526086, 0.7297120527259999, 0.6797915354981483, 0.5578388055854854, 0.42212508190963766, 0.4728519279562826, 0.660065545433877, 0.8304731915277361, 0.8688908254782514, 0.7911743460205212, 0.6672402813571379, 0.6540889113402244, 0.7668402779686581, 0.8777695221868312, 0.6742608531261972, 0.55982342726776, 0.2111731628644695, 0.21964166124943402, 0.2406348627525607, 0.2342140205540891, 0.41564310120480824, 0.5958835895646388, 0.572122740483245, 0.539569566132146, 0.5912296055436914, 0.6707941646262765, 0.7551437301742864, 0.7445973377251311, 0.690459084874388, 0.6638078893386712, 0.6109803186034004, 0.49254907068128556, 0.39335932614582914, 0.5056186497104705, 0.7966487048832958, 0.8787489652201512, 0.874712944991343, 0.8369217713986431, 0.6973430006919593, 0.501407968506318, 0.40491626691336996, 0.3481579134794845, 0.3410313444169036, 0.39400627948584976, 0.49140545700720945, 0.6704215433898681, 0.8042544170501448, 0.8854267540835039, 0.8432183898023096, 0.8237706656252947, 0.8543990761318925, 0.8012126297192188, 0.5671308587865225, 0.458991645549746, 0.18599736085423013, 0.1449125308756743, 0.03394630567399466, 0.0074150533578610615, 0.15201500081530867, 0.28117181559173077, 0.3396215326012667, 0.4225538870670107, 0.5430018145867008, 0.634897002134175, 0.6747177182502399, 0.5080658735820608, 0.36815793666298857, 0.49353378005005016, 0.6420250824104837, 0.632144554138181, 0.52272079161042, 0.5134270669619547, 0.6865006512186288, 0.8076851184312474, 0.8458725930331311, 0.7903279528769357, 0.5475037117703913, 0.24400085196500515, 0.10922237022595775, 0.09747636856683953, 0.15888391920485098, 0.17101525754479968, 0.211555563509814, 0.3418960458036017, 0.5638521263267628, 0.8295121974917624, 0.9155092755985514, 0.9221847678153645, 0.9250716537573607, 0.7703030549509282, 0.4691086331883348, 0.36930585385200276, 0.3149779154677299, 0.24024045425188523, 0.03770480531578218, -0.0034250267074730965, 0.1235881399600007, 0.10249112451399482, 0.1477046379933148, 0.3168593676359161, 0.5413824741274937, 0.6794054892664699, 0.7275680102436659, 0.48001102149988406, 0.12813444906437668, 0.22733114346071032, 0.5381085470326341, 0.7416713420736248, 0.7020421075491264, 0.5680740149439093, 0.45380591135111, 0.5311118372943365, 0.6175931851513337, 0.6131629212797205, 0.44040676271862034, 0.24386399593504193, 0.15971852005755863, 0.1314553096739919, 0.1495885883772675, 0.17058614344629097, 0.25057344173809043, 0.34721104193032787, 0.435636602947821, 0.5579500976787258, 0.6951254736197132, 0.7901409850302084, 0.8588182141780586, 0.6799009137413315, 0.3870578109047032, 0.33005318449083293, 0.4203511985298797, 0.3743867284778113, 0.22017713409813452, 0.25969551644833394, 0.4162446423103552, 0.26630913619958685, 0.23580544549110086, 0.44933973716980113, 0.7066475430091171, 0.8426417401085793, 0.8730883471202815, 0.6437587590105098, 0.2265706632284044, 0.24305765160764392, 0.554451780620272, 0.7828524730046583, 0.7793343048993668, 0.563214399570922, 0.31235157851341294, 0.42343797392377397, 0.5133211411359173, 0.5768754806179459, 0.5924417860559511, 0.5232364434557537, 0.4407756511315887, 0.35050970900936446, 0.29271341405548107, 0.35686068358272044, 0.41656891075911595, 0.41970637778084774, 0.3612274587951998, 0.3057784052082909, 0.3539849325161121, 0.45173566246449337, 0.5397156059523001, 0.3990587663601118, 0.2665477317446103, 0.273672772731938, 0.34714649668839376, 0.34813233864804494, 0.2944453443449099, 0.3741689569186266, 0.6541844067030714, 0.5964112667165241, 0.5307847273330228, 0.7112030998388538, 0.9102512680442523, 0.9869908938378065, 0.9533134628974899, 0.6958996850407326, 0.404369342746034, 0.42853733108238384, 0.6346363085808423, 0.7761026820700546, 0.7405111053350951, 0.48087294798440955, 0.2843787899258074, 0.3981505444451862, 0.5120696451735527, 0.662091972662563, 0.8175091367051257, 0.8061153796101843, 0.6736367396021047, 0.4746491746329281, 0.33083374144457833, 0.40198860931557817, 0.45314069641432175, 0.3889135809427025, 0.2394251212937652, 0.11286517219105478, 0.11801018088702117, 0.20162418890476708, 0.30654754524693895, 0.26112546303682893, 0.2155327474567719, 0.25280529172651794, 0.25003078992493566, 0.25514089745212776, 0.23219231384728867, 0.3230677293529157, 0.6685118614035493, 0.7177962614559221, 0.646449276025266, 0.7705175367169201, 0.8864298845326639, 0.9289264377665761, 0.9179608080317324, 0.769954204065185, 0.6234585253075666, 0.6351692196475374, 0.7301873742347361, 0.7417263968249659, 0.6669821743035135, 0.43509668109877314, 0.30043957561470896, 0.3788105430539696, 0.46764085632127106, 0.6218502988414353, 0.8138479635012615, 0.8396462915064934, 0.6804701222976216, 0.4108897484958649, 0.26656369387504575, 0.4035224198617804, 0.47289354741805334, 0.3961989743565775, 0.26981874361303126, 0.14765139535061292, 0.11490109178115271, 0.1782388546048473, 0.29433607758214897, 0.33746440998915855, 0.27774691888396136, 0.30265223123829643, 0.24780308962591124, 0.24029447534030265, 0.18255018631819656, 0.2764813207719003, 0.6136651527821828, 0.6380034565791759, 0.5133134903691413, 0.6123415906315393, 0.7065884357300758, 0.7510799650904458, 0.7898642726945704, 0.7802898452947128, 0.7711717613465999, 0.7926738060864146, 0.832488915206862, 0.7556911275486993, 0.6302846048875063, 0.4494600124836901, 0.3762817180802865, 0.40948904010926895, 0.41315116713445416, 0.49806624936661575, 0.6547064370184769, 0.7165195957207734, 0.5875159172001054, 0.31658988917523573, 0.2305293911583405, 0.46049455794606586, 0.5460360800501763, 0.44684895024121757, 0.3589183922783645, 0.26183119970853774, 0.198706953491454, 0.22309857555176776, 0.32700783832302316, 0.39910884815376324, 0.3185416052354477, 0.3304951872270672, 0.32142984692042975, 0.29400761858803054, 0.1991301690988261, 0.3221529572641738, 0.6565360385624355, 0.587748135360261, 0.3190096669973506, 0.35300940244015316, 0.4709256001463714, 0.5436007799074213, 0.6298829200538323, 0.7365240813726998, 0.8429150316740247, 0.8946954813694424, 0.9076219927564182, 0.8056685142072854, 0.6431065690704951, 0.5042031297030932, 0.517924106678352, 0.5014734490102681, 0.39904849457013597, 0.37100517095117286, 0.45197019302321445, 0.5402057961383067, 0.46153679653880353, 0.21657033077203755, 0.18679972744919388, 0.5130159523010114, 0.6411795101590703, 0.5333639759878224, 0.4369335727106605, 0.3447818487630748, 0.25917782936578004, 0.24354695819402233, 0.3038479462519675, 0.37833624753393297, 0.3139540552636098, 0.3174143342525395, 0.4893129703675937, 0.4557100823661588, 0.3674366676952696, 0.5138078070828694, 0.8330611243862623, 0.6884485640779557, 0.2728510836746932, 0.13534875067782998, 0.24057730639843372, 0.34694380643323286, 0.47810095418322063, 0.6495409323964011, 0.7939946092622513, 0.889062404719307, 0.9258536978196241, 0.8649615112754476, 0.7178113522312337, 0.6063932370741941, 0.7192577049404074, 0.682779152243775, 0.484743135084877, 0.32927106247958315, 0.28632321155191653, 0.334502781390674, 0.2973165654167363, 0.1259777813974857, 0.10989186745314206, 0.4361158671826699, 0.6257042879169155, 0.6412391159064941, 0.5474317145458498, 0.38379226038756614, 0.2156134228209718, 0.15021678759978574, 0.17899100338480883, 0.269724551914344, 0.25624150123814377, 0.26447484049424586, 0.6804156212872999, 0.6515149918926652, 0.5620623152882379, 0.594469530670357, 0.8402345408793951, 0.8124436834084651, 0.4893807330474828, 0.24467741673037385, 0.2681887342925172, 0.35001606066735563, 0.4495181649025, 0.5061220070019199, 0.5345563317261156, 0.6507995900720287, 0.7606813814160734, 0.8073900448833561, 0.7614653964773938, 0.7289966901777104, 0.884103837582791, 0.8420290597782556, 0.6270227592315788, 0.4239145282897676, 0.28855571748946923, 0.29572687940796455, 0.3102952006154108, 0.2269814065339386, 0.12410888853612326, 0.27957601952381295, 0.5551996745316914, 0.7604927446628489, 0.753892825588626, 0.5451618453252096, 0.3138624392827321, 0.23111562818294265, 0.251484407195052, 0.3193124990920135, 0.29906139436889034, 0.3160243478999383, 0.7199527239035522, 0.6780134623353664, 0.5516936887526374, 0.4593290660964186, 0.59152073650529, 0.7192383269473447, 0.5967033378686395, 0.385516741454076, 0.3695198997868462, 0.41841576775927514, 0.4534267927272358, 0.3699688533549714, 0.3588114578323603, 0.4641730216603769, 0.5666136383763225, 0.6519504655449916, 0.7179314454474015, 0.795897681234244, 0.9771398161802356, 0.8753988879566029, 0.6689586505896128, 0.4926170932514045, 0.38317672419973586, 0.43576742942155383, 0.5011694580574997, 0.47298586218848443, 0.31470130836495663, 0.32708799138317685, 0.5655845326888224, 0.7615585717420454, 0.7740167738466899, 0.6294033380169237, 0.5091243226751088, 0.4721891865341814, 0.4595866682817182, 0.4626668996198426, 0.42502439923167, 0.4180437474608611,
                 0.5171763545964596, 0.47380223928988174, 0.34455760629289606, 0.2181513800015869, 0.28127947371849027, 0.4391898133800182, 0.46810778849069595, 0.346030501648432, 0.31115082997294213, 0.3370964038168936, 0.36006589108161685, 0.3430535419611743, 0.42245307370308793, 0.5043015866230481, 0.4807669450960035, 0.4377872506100413, 0.5555822473475561, 0.7296214031782428, 0.9215677711158693, 0.8375273018996083, 0.6729067654044398, 0.5627659848981187, 0.54674186905082, 0.6649126067532191, 0.7572906699555818, 0.745016427246099, 0.615485699749631, 0.5179181319603635, 0.5630070298288975, 0.6268414789237327, 0.5836352129545589, 0.5165591505609459, 0.5828666479709523, 0.6332592884359566, 0.6347386923605716, 0.5790358088757265, 0.47627779693708033, 0.4342879632916509, 0.2339671433203152, 0.22047148238475625, 0.1731822288739769, 0.10135481216607821, 0.13386761575418826, 0.2605484550506164, 0.2789694163001314, 0.19780562444287467, 0.17769038906874124, 0.21030740358647065, 0.2764484889378287, 0.43132905160712653, 0.627771968334074, 0.6581911860799736, 0.47219452642304294, 0.2320450641821201, 0.28643932445504416, 0.5708358505310044, 0.7888057070257637, 0.7412118821343046, 0.6347460335577076, 0.5910766323758808, 0.6503728735277159, 0.7946192354907056, 0.8916648567914015, 0.9055381322579482, 0.8517679969946033, 0.7274563363574603, 0.5600466650879455, 0.4242002788463237, 0.3209655856876592, 0.27817935180787196, 0.43166787469739953, 0.6031733841189625, 0.7132285490781476, 0.6561335954359875, 0.4667893374482603, 0.3987600354975067, 0.22231853517701933, 0.2454614725995865, 0.29045018904042336, 0.31742720762121807, 0.30132304734015947, 0.3076989021945374, 0.2437044247682493, 0.20730436366443356, 0.24116345889598395, 0.2698574521193776, 0.30759648383278704, 0.4961880438742654, 0.7264451175521831, 0.7012820129532988, 0.43785815490612295, 0.12538378697596816, 0.12958672446250974, 0.47552167979884585, 0.7271679200602071, 0.6231641367745011, 0.5337562204033074, 0.5405820538605408, 0.6306129618435387, 0.7348116525667542, 0.8318622183533024, 0.8965741234551426, 0.9208971263253862, 0.858829166824644, 0.651740880627483, 0.42945753850526774, 0.28433111745118933, 0.24863793624850714, 0.3714278080096565, 0.5414283934712598, 0.672910943951201, 0.6426554777336477, 0.45314893458424826, 0.3799862951060636, 0.46862132763785885, 0.5025087929652683, 0.5829794442980714, 0.717360245962937, 0.6869239199668958, 0.5012834071876097, 0.3301760496195876, 0.3326297684526697, 0.3881985287740194, 0.4014196058599129, 0.3874292908233945, 0.4991777896736987, 0.6607136633111387, 0.6285800641137845, 0.4307255817422782, 0.1726831134139277, 0.15217040676485427, 0.40455729060322204, 0.6128309868905546, 0.49037029988849823, 0.418852458384062, 0.4438347188096443, 0.5440987824719901, 0.6159667952920409, 0.6688816848349719, 0.7054299542387209, 0.773594233668516, 0.8459019316433142, 0.7862215278810039, 0.6348489768475296, 0.480285669463737, 0.4330089745444375, 0.48819805122357307, 0.5219352842201261, 0.5167418236273827, 0.48062537831468616, 0.3513951442518388, 0.29119118630500745, 0.7727908327883367, 0.794742657187643, 0.8271525202011711, 0.9450974266826448, 0.9319014590073973, 0.6472186538222731, 0.4080170357814263, 0.4476332185731068, 0.4903891390259073, 0.4990315678980439, 0.47291684175595566, 0.49291235732595323, 0.5702060836266878, 0.5853396715709134, 0.5829789499672866, 0.46005345913157536, 0.3337109187544151, 0.34779047000456276, 0.41428030236274926, 0.30414985616146883, 0.2936728925602451, 0.34430126461159405, 0.43835922006526035, 0.5143871352725141, 0.5331515322980842, 0.5152410602349015, 0.5549893739031277, 0.7016514062563516, 0.7954928114454451, 0.7524572832503936, 0.6520352586579958, 0.6059715646233699, 0.56164410670553, 0.4528397826157279, 0.3441614853802738, 0.28758550092390234, 0.22342524257929539, 0.1938253535847293, 0.7844023409137725, 0.7782586903094931, 0.7592533435644214, 0.8191277344121184, 0.8931468630754141, 0.7260500304329469, 0.4901631842699602, 0.4574219771339299, 0.4715289097905507, 0.4932641707168859, 0.5105361717741611, 0.5967506661013328, 0.6989801727313196, 0.7098967786158924, 0.7782675147777302, 0.7634033063270566, 0.6038128193487127, 0.428105836160753, 0.3489944360267045, 0.2410582022365534, 0.2527096086517205, 0.3164844749114429, 0.38634864335682495, 0.38107026376337416, 0.34247930779440944, 0.3011296939941926, 0.3085126650002678, 0.38870757718446597, 0.519461061390947, 0.5682282919399088, 0.5202407202014685, 0.45748494562892006, 0.43724922477587586, 0.4173810528356698, 0.39426604514582986, 0.31490860428855566, 0.2613298736212798, 0.29609624100847354, 0.4865611359730277, 0.4520694982982668, 0.415881634039621, 0.579137041595857, 0.8855218472056018, 0.7901582930568748, 0.5467621909800775, 0.45822752357082325, 0.48224411094792063, 0.5056203496129951, 0.5283612662052118, 0.6330022596861569, 0.7539460793312011, 0.7759324131769744, 0.8093561450429553, 0.8102000172479127, 0.7095523916084471, 0.555956170490956, 0.4245930982711298, 0.3305508679782826, 0.38286183867381945, 0.4535046575550824, 0.4686951804391834, 0.3526540053031882, 0.18544837538006334, 0.010704896319937261, 0.0133632661143813, 0.14728363543913756, 0.34121102854380725, 0.41130699332375875, 0.28610998534004045, 0.18043415080507255, 0.3014316834640359, 0.48934425903980333, 0.6373678056177153, 0.6112558251576513, 0.5198329072243337, 0.5293417298257423, 0.3043384112186402, 0.28054087706727365, 0.3179371587599385, 0.6321759042245512, 0.9119218936669697, 0.7214429231993129, 0.4667398257083629, 0.4605091721348761, 0.5548586449486854, 0.5847060024422052, 0.5628592217057344, 0.4699556667943035, 0.5294413700242836, 0.7483326123853669, 0.8738885441698423, 0.889803971109292, 0.7911550282176539, 0.6521736427952047, 0.5345849351745825, 0.4610998142559175, 0.558492350361115, 0.636726907503286, 0.5943500969633784, 0.3833144402058119, 0.1502448487359015, -0.04367656888414538, -0.0007028201484312068, 0.21238881230646675, 0.39754323988873647, 0.38613358401058934, 0.1956850558473772, 0.10371222394978681, 0.3130219898701381, 0.5736152043260195, 0.7525080947493399, 0.6856673317169161, 0.565168507802502, 0.5338359417684188, 0.30452200108667815, 0.29848791648545386, 0.37975257260454115, 0.7289127543371416, 0.8886901913541965, 0.6374249269210622, 0.4064886085460859, 0.4893688723542869, 0.6369721314916125, 0.6672247735470745, 0.5960499355511384, 0.3436744125008977, 0.3701878581767844, 0.6934951694891687, 0.8744583413885294, 0.9196080255719452, 0.8756402837990774, 0.7371489420216085, 0.5678837014770937, 0.4973924267279776, 0.5927429876484073, 0.683637185037031, 0.6585747463387549, 0.4339510863337969, 0.19595179255994266, 0.030877002088263657, 0.07104188589888992, 0.26046135521486236, 0.36751047747221327, 0.3111696159905046, 0.17364595692293966, 0.17396869614330707, 0.4086589836283947, 0.6247428701717692, 0.7443035984674586, 0.6243211185196194, 0.48872466708204393, 0.4497828334123634, 0.3932954643820757, 0.3937600278171799, 0.47105731297477577, 0.7921896448861985, 0.8333633398060865, 0.5570204580510729, 0.3656292646294686, 0.5192152015540772, 0.7256512190690815, 0.7545540149338873, 0.6351336349065194, 0.2882375867508048, 0.25799326322626914, 0.5759923885433558, 0.787442295619985, 0.8651568383659607, 0.8799510041329723, 0.7657259436199623, 0.553980414065768, 0.4468201825433515, 0.5153553961436741, 0.6286475872286894, 0.6878090836053485, 0.5342118818935951, 0.32839526070649566, 0.16581081672916784, 0.14698793757132994, 0.2702280513570772, 0.31097543316532883, 0.22734814450971733, 0.16267474037425683, 0.2784756358282356, 0.5228198616268881, 0.6643363025842828, 0.7087645714502273, 0.5617470358426957, 0.4292189108966861, 0.3894344664159504, 0.5885298200584955, 0.5807527175821868, 0.6056319952060832, 0.7446528496247966, 0.6443107493080585, 0.46061682344555344, 0.29521450984689546, 0.41473376229949016, 0.7127547952149077, 0.8114416630985158, 0.7298689468014513, 0.3690928828937791, 0.2239966290155331, 0.36839327916291237, 0.5304564742386652, 0.6382575767997029, 0.7006865972210544, 0.6911819865825193, 0.523363899435806, 0.28396742585879475, 0.2761490686091884, 0.42444750027818834, 0.6386754989995889, 0.6477870991362591, 0.5100814842675847, 0.3774803133411641, 0.38091088032638565, 0.44627004513511453, 0.44685470666310634, 0.32812012539786706, 0.242724320817625, 0.3701529379535617, 0.6036324991268206, 0.7092773170155822, 0.707063352296823, 0.5739217845581455, 0.5043881391213176, 0.4665500924705326, 0.5153900271095898, 0.5139130620186906, 0.5191360549860158, 0.48380677859821164, 0.4726027838872465, 0.4933104236896218, 0.3056817537460939, 0.19195577128985078, 0.3748826746072249, 0.4767408643595558, 0.5039163264010962, 0.36848790449671526, 0.28144056731790024, 0.20979453278081825, 0.15406009259130612, 0.22840007339179125, 0.4361219248334532, 0.657341206134149, 0.6261800734510872, 0.3364361168636877, 0.24177815828891763, 0.31839175121357777, 0.500093940602464, 0.5597739242475208, 0.4720008402253657, 0.4551827010890551, 0.6508050201278823, 0.7683477566966697, 0.7469214280576748, 0.6207570714871917, 0.5278091531649101, 0.6155934304752877, 0.8064020158193596, 0.8811167891362084, 0.8620627864792911, 0.7302492562753428, 0.6430152157290213, 0.6004513861194829, 0.341191559099761, 0.3517913411912167, 0.3701213988699447, 0.3165570723349899, 0.449095123860973, 0.5839127730459185, 0.42463866331061473, 0.14408908478456534, 0.06278585597230714, 0.08257704699019465, 0.17243430971018697, 0.3227514133896391, 0.5074403195938356, 0.40728108669536706, 0.22024290499801608, 0.2070213625582937, 0.4408469384552566, 0.7478556091374267, 0.7106950102234754, 0.4226041101991786, 0.3462386993923008, 0.38708640771628194, 0.4967368024141628, 0.5088260661959149, 0.41796960610454925, 0.40872362953494584, 0.6173155960071801, 0.7273159354446381, 0.6583500998912196, 0.549378874529544, 0.5026332600228397, 0.6259416746683825, 0.8085433757936065, 0.8822208659629511, 0.910492964538238, 0.8073041734490738, 0.6972209501279477, 0.6773738765114893, 0.3788057684690594, 0.3971211326336113, 0.43584108051827053, 0.35602078394945125, 0.4411309120947702, 0.6132494927958684, 0.4972723847352579, 0.193220280731553, 0.027071420596388302, 0.0050707438907669775, 0.1001768385192302, 0.33982791524318545, 0.7038319955605986, 0.6330739044012058, 0.3704853187507019, 0.3020417314407098, 0.5253480177550474, 0.7921129039536354, 0.6887511249367639, 0.4214062845878511, 0.3799816800841086, 0.4220389447047756, 0.484994509365, 0.4120834847492024, 0.29277729722304324, 0.2797215165403391, 0.46168147451757763, 0.5479550266627009, 0.4511780437143694, 0.3643513886136958, 0.3481224376896087, 0.46533066448740174, 0.6245207388888141, 0.7131210747277684, 0.7709206041220178, 0.7140938083238614, 0.6813641759222965, 0.6986710330774687, 0.5659321330636107, 0.5940160810070638, 0.6404671988378143, 0.5055001131729036, 0.45828993444354793, 0.6174322541898867, 0.5617934552176047, 0.27656436415661306, 0.09640387969134215, 0.06491133278333593, 0.1582814387443097, 0.4173267592389569, 0.8289744109667642, 0.7477706878330088, 0.4348507480696171, 0.34066424911500975, 0.5662288417987131, 0.7518336272403272, 0.6223938391052192, 0.4269055710523423, 0.4216606069719703, 0.45205595278619615, 0.4403427702499593, 0.28508898990883785, 0.1411586930045726, 0.11387303246858262, 0.26349549152836327, 0.34977295559509464, 0.2964891735560568, 0.26315270100715316, 0.2624292417724123, 0.2888691177539309, 0.3556405382544058, 0.46508753602594666, 0.5578468562632962, 0.5745312382485128, 0.6334363113335899, 0.6816128838179367, 0.786749352807253, 0.8324110979078381, 0.9177552178342123, 0.7194359169913102, 0.4072771119788737, 0.4661407543007918, 0.5171243069451281, 0.36774946254321883, 0.23934822731712763, 0.21498623378533918, 0.2890189276688078, 0.5608850938953585, 0.8507574203114688, 0.6261390003647368, 0.25891554946893475, 0.177037903850729, 0.46401896139282717, 0.6380983716497507, 0.5388612226391285, 0.4541343274295478, 0.5038152609852472, 0.5364999851082785, 0.4841170288466517, 0.3101037622432054, 0.1538313273195209, 0.11338326004798222, 0.17882227820630955, 0.22360776271272367, 0.32938896633632625, 0.4595938069796543, 0.49177085972224677, 0.33686823791445997, 0.13228668971105778, 0.16045670188015537, 0.2990937949272492, 0.44051994606692807, 0.5497125633085908, 0.6131117990485454, 0.7206517758883071, 0.7587842805092536, 0.8329641932033671, 0.6488258509491864, 0.27155415442927044, 0.2863605316946072, 0.4842828558435759, 0.4383636924029558, 0.3408425353455445, 0.3075122476428913, 0.32460979224435177, 0.47185846003138593, 0.6301261115305238, 0.4981713764443708, 0.20942573176239157, 0.1199488324047473, 0.3348889047915269, 0.5527208974259196, 0.5415669030724769, 0.4961070954880621, 0.5495712337098978, 0.6118281576290177, 0.6587852339039472, 0.5899750019271301, 0.4819327322265109, 0.4230843595591998, 0.3094673813832295, 0.21941798699640822, 0.3609338752022167, 0.62572945809292, 0.8144077747568024, 0.6656172739247102, 0.24494750849327201, 0.10841858375864888, 0.21712343479514937, 0.45630710207062286, 0.5363465380727578, 0.5631169714462543, 0.7419876285435886, 0.7621277668460624, 0.7700923997226775, 0.5293647740231512, 0.2139494428557547, 0.3264723272249587, 0.577570955319407, 0.5096678388134742, 0.40415852465285573, 0.35522543473161444, 0.3246633813698639, 0.34191332888540793, 0.42810846774925543, 0.4133876536244241, 0.24997914828717405, 0.17124408101238858, 0.3068003948363281, 0.5408016246994575, 0.5062217890358895, 0.3886383033602096, 0.41862529323114106, 0.4963457367995278, 0.6123476654845612, 0.6544593155148395, 0.637080385580899, 0.5993634251904523, 0.3923747849600426, 0.1782732446006359, 0.26004534507902977, 0.5263556328508462, 0.7875414456025134, 0.7060328843994876, 0.283910459769895, 0.1437424351392077, 0.26941516285522704, 0.5650157070262194, 0.610105667178569, 0.6002111424368223, 0.7576389211968648, 0.7723371874863205, 0.7577528617541504, 0.4709777431317903, 0.16926665563959112, 0.3293870691388987, 0.6052254786657126, 0.5446827281838325, 0.4392814320249284, 0.379181012878921, 0.32494911020019174, 0.29531172653794996, 0.3598250029529492, 0.37961685686409047, 0.26318585461490973, 0.18506659011424434, 0.31057287975875786, 0.5547340086950856, 0.49136838121110715, 0.3433490991749213, 0.3621662944483291, 0.4416656403764211, 0.573998628790775, 0.6595998703190874, 0.6911096768370247, 0.6825133649550056, 0.46794425431495723, 0.19464433101221423, 0.23252511688794497, 0.4919840451691846, 0.7595815764181019, 0.6901765883226276, 0.28201455275886417, 0.15489084258316382, 0.2894851499575413, 0.6070988258033962, 0.6434692637003615, 0.6258057997029263])
    kx = 3
    ky = 3

    # x = np.array([0, 1.2, 1.4])
    # y = np.array([0,0.1])

    x = np.array([0.1])
    y = np.array([0.1])

    A = scipy.interpolate.bisplev(x, y, (tx, ty, c, kx, ky))
    B = fpbisp(tx, ty, c, kx, ky, x, y)

    print(A)
    print(B)

    assert np.all(A == B)