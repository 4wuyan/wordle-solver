#!/usr/bin/env python3

"""
A wordle solver

Example usage:
python3 wordle-solver.py black=01122 white=01122

(0 for grey, 1 for yellow, 2 for green)
"""

import argparse
import re
import sys
from collections import defaultdict


def main():
    tries = parse_arguments()
    global_clues = defaultdict(Clue)
    for attempt in tries:
        new_clues = get_clues(attempt)
        for letter, new_clue in new_clues.items():
            global_clues[letter] += new_clue

    rules = []
    for letter, clue in global_clues.items():
        rules += get_rules(letter, clue)
    for c in filter(lambda x: all(r(x) for r in rules), five_letter_words):
        print(c)


def get_clues(attempt: str):
    word, outputs = attempt.split('=')
    result = defaultdict(Clue)
    for i, (letter, output) in enumerate(zip(word, outputs)):
        if output == '0':
            result[letter].may_have_more = False
        else:
            result[letter].min_occurrence += 1
            if output == '1':
                result[letter].must_not_be_at.append(i)
            else:
                result[letter].must_be_at.append(i)
    return result


def get_rules(letter, clue):
    result = [lambda x, le=letter, p=p: x[p] == le for p in clue.must_be_at]
    result += [lambda x, le=letter, p=p: x[p] != le for p in clue.must_not_be_at]
    if clue.may_have_more:
        result.append(lambda x, l=letter, c=clue.min_occurrence: x.count(l) >= c)
    else:
        result.append(lambda x, l=letter, c=clue.min_occurrence: x.count(l) == c)
    return result


class Clue:
    def __init__(self):
        self.min_occurrence = 0
        self.may_have_more = True
        self.must_be_at = []
        self.must_not_be_at = []

    def __add__(self, other):
        result = Clue()
        result.min_occurrence = max(self.min_occurrence, other.min_occurrence)
        result.may_have_more = all([self.may_have_more, other.may_have_more])
        result.must_be_at = self.must_be_at + other.must_be_at
        result.must_not_be_at = self.must_not_be_at + other.must_not_be_at
        return result


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('tries', nargs='+',
                        help='Previous attempts. Format: "words=00112". 0 for grey, 1 for yellow, 2 for green.')
    tries = [t.lower() for t in parser.parse_args().tries]
    pattern = re.compile('^[a-z]{5}=[0-2]{5}$')
    if all(map(pattern.match, tries)):
        return tries
    else:
        parser.print_help()
        sys.exit(1)


# From https://github.com/dwyl/english-words/blob/master/words.txt
five_letter_words = '''
aahed abaci aback abaft abase abash abate abbes abbey abbot abeam abets abhor abide abler ables abner abode aboil abort
about above abuse abuts abuzz abyes abysm abyss accts acerb ached aches achoo acids acidy acing acmes acned acnes acoin
acorn acred acres acrid acted actin actor acute adage adams adapt addax added adder addle adept adieu adios adits adman
admen admin admit admix adobe adolf adopt adore adorn adoze adult adyta adzes aegis aeons aerie aesop afars affix afire
afoot afore afoul afrit afros after again agama agape agars agate agave agaze agent agers aggie aghas agile aging agist
aglee aglet agley aglow agone agons agony agora agree agric agues ahead ahems ahold aided aider aides ailed aimed aimer
ainus aired airer aisle aitch ajiva akron alack alamo alans alarm alary alate album alder alecs alefs aleph alert alfas
algae algal algas algid algin alias alibi alice alien align alike aline alive alkyd alkyl allah allay allen aller alley
allot allow alloy aloes aloft aloha alone along aloof aloud alpha altar alter altho altos alums alway amahs amain amass
amaze amber amble ameba ameer amend amens ament amias amice amici amide amids amies amigo amino amire amirs amish amiss
amity ammos amoks amole among amort amour amove ample amply ampul amuck amuse amyls andes andre anear anele anent angas
angel anger angle anglo angry angst angus anile anils anima animo anion anise ankhs ankle ankus annal annas annat annex
annie annoy annul annum anode anoia anole anomy anted antes antic antis antra antre anvil aorta aouad apace apart apeak
apeek apers apery aphid aphis apian aping apish apium apnea aport appal apple apply apres april apron apses apter aptly
aquae aquas arabs araks arbor arced arcus ardor areal areas arena arete argal argle argon argot argue argus arhat arias
ariel aries arils arise arith armed armer armor aroma arose arras array arrow arses arsis arson arums aryan aryls ascii
ascot ashed ashen ashes asian aside asked asker askew aspca aspen asper aspic assam assay asses asset assoc aster astir
asyla async ataxy atilt atlas atman atmas atoll atoms atomy atone atria atrip attar attic audad audio audit auger aught
augur aunts aunty aurae aural auras auric aurum autos autre auxin avail avast avers avert avian avion aviso avoid avows
awacs await awake award aware awash awful awing awned awoke awols axels axial axils axing axiom axled axles axman axmen
axone axons ayahs azide azido azine azoic azole azons azote azoth aztec azure baaed baals babas babel babes babka baboo
babul babus bacca backs bacon baddy badge badly bagel baggy bahts bails bairn baits baize baked baker bakes balds baled
baler bales balks balky ballo balls bally balms balmy balsa banal banco bands bandy baned banes bangs banjo banks banns
bantu barbs bards bared barer bares barfs barge baric barks barky barmy barns barny baron barre basal based baser bases
basic basil basin basis basks bassi basso bassy baste basts batch bated bates bathe baths batik baton batts batty bauds
baulk bawds bawdy bawls bayed bayou bazar beach beads beady beaks beaky beams beamy beano beans beard bears beast beats
beaus beaut beaux bebop becks bedew bedim beech beefs beefy beeps beers beery beets befit befog began begat beget begin
begot begum begun beige beigy being belay belch belie belle belli bello bells belly below belts bemas bemix bench bends
bendy benes benin benny bents beret bergh bergs berms berry berth beryl beset besom besot bests betas betel betes beths
betta betty bevel bewig bezel bhang bialy bibbs bible biddy bided bider bides bidet biens biers biffs biffy bifid bight
bigly bigot bijou biked biker bikes bilbo biles bilge bilgy bilks bills billy bimah binal binds bines binge bingo bints
biome biont biota biped bipod birch birds birth bison bitch biter bites bitsy bitte bitts bitty blabs black blade blahs
blain blame blanc bland blank blare blase blast blats blaze bleak blear bleat bleed bleep blend blent bless blest blimp
blimy blind blini blink blips bliss blitz bloat blobs block blocs bloke blond blood bloom bloop blots blown blows blowy
blued bluer blues bluet bluey bluff blunt blurb blurs blurt blush board boars boast boats bobby bocce bocci boche bocks
boded bodes boers boffo boffs bogey boggy bogie bogle bogus boils boise bolas boles bolls bolos bolts bolus bombe bombs
bonds boned boner bones boney bongo bongs bonny bonos bonum bonus bonze boobs booby booed books booms boomy boons boors
boost booth boots booty booze boozy borax bored bores boric borne boron borts borty bortz bosks bosky bosom boson bossa
bossy bosun botch bough boule bound bourg bourn bouse bousy bouts bovid bowed bowel bower bowie bowls bowse boxed boxer
boxes boyos bozos brace bract brads braes brags braid brail brain brake braky brand brans brash brass brats brave bravo
brawl brawn brays braze bread break bream brede breed brent breve brevi brews brian briar bribe brick bride brief brier
bries brigs brill brims brine bring brink briny brios brisk broad brock broil broke bromo bronc bronx brood brook broom
broth brown brows bruce bruin bruit brunt brush brusk brute bryan bubby buchu bucko bucks buddy budge buffo buffs buffy
buggy bugle buick build built bulbs bulge bulgy bulks bulky bulls bully bumps bumpy bunch bunco bunds bungs bunko bunks
bunns bunny bunts buoys burgh burgs burin burke burls burly burma burns burnt burps burro burrs burry bursa burse burst
busby bused buses bushy busts busty butch butte butts butty butyl buxom buyer bwana bylaw byres byron bytes byway cabal
cabby caber cabin cable cabob cabot cacao cache cacti caddy cades cadet cadge cadgy cadis cadre cafes caged cager cages
cagey cains cairn cairo cajon cajun caked cakes calfs calif calix calks calla calli calls calms calor calve calyx camel
cameo campi campo camps campy canal candy caned caner canes canna canny canoe canon canst canto cants canty caped caper
capes capon capos cappy caput carat carbo cards cared carer cares caret cargo carlo carne carny carob carol carom carpe
carpi carps carry carte carts carve casas cased cases casks caste casts casus catch cater cates cathy catty caulk cauls
cause caved caver caves cavie cavil cawed cease cecal cecil cecum cedar ceded ceder cedes ceils celeb celli cello cells
celts cense cento cents cered ceres ceria chads chafe chaff chain chair chalk champ chams chang chant chaos chaps chapt
chard chare charm chars chart chary chase chasm chats chaws cheap cheat check cheek cheep cheer chefs chela chert chess
chest chevy chews chewy chiao chias chick chico chics chide chief chiel child chile chili chill chime chimp china chine
chink chino chins chips chirk chirp chits chive chivy chock choir choke choky chomp chops chord chore chose chows chubs
chuck chuff chugs chump chums chunk churl churn chute chyme cider cigar cilia cinch cines cions circa circe cists cited
citer cites civet civic civil civvy clack clads clags claim clair clamp clams clang clank clans claps clapt clark clash
clasp class claus clave claws clays clean clear cleat clefs cleft clepe clept clerk clews click cliff clift climb clime
cline cling clink clips clipt cloak clock clods clogs clomb clomp clone clonk clops close cloth clots cloud clout clove
clown cloys clubs cluck clued clues clump clung clunk coach coact coals coast coati coats cobby cobol cobra cocas cocci
cocks cocky cocoa cocos codal codas coded coder codes codex codon coeds coffs cohen cohos coifs coign coils coins coirs
coked cokes colas colds coles colic colin colly colon color colts comas combe combo combs comer comes comet comfy comic
comma comme commy comps compt comte conch condo coned cones coney conga congo conic conks conky conns conte conto conus
cooch cooed cooee cooer cooey cooks cooky cools cooly coomb coons coops coopt coots copal coped coper copes copra copse
coral cords cored corer cores corgi corks corky corms corns cornu corny corps corse cosec coset cosey cosie cosmo costs
cotan coted cotes cotta couch cough could count coupe coups court couth coved coven cover coves covet covey cowed cower
cowls cowry coyer coyly coypu cozen cozes cozey cozie craal crabs crack craft crags cramp crams crane crank crape craps
crash crass crate crave crawl craws craze crazy creak cream credo creed creek creel creep crees creme crepe crept crepy
cress crest crete crews cribs crick cried crier cries crime crimp crisp croak croci crock croft crone crony crook croon
crops cross croup crowd crown crows crude cruds cruel cruet crumb crump cruse crush crust crypt cuban cubby cubed cuber
cubes cubic cubit cuddy cuffs cuing cuish cukes culls cully culms culpa cults cumin cunni cunts cupid cuppa cuppy curbs
curds curdy cured curer cures curia curie curio curls curly curry curse curst curve curvy cushy cusps cuter cutes cutey
cutie cutin cutis cutty cutup cyans cycad cycle cyclo cymes cynic cysts czars czech daces dacha dadas daddy dados daffy
dagos daily dairy daisy dales dally dames damns damps dance dandy danes dangs dante dared darer dares darks darky darns
darts dashy dated dater dates datum daubs dauby daunt david davis davit dawns dazed dazes deads deair deals dealt deans
dears deary deash death debar debit debts debug debut decal decay decks decor decoy decry deeds deedy deems deeps deers
defat defer defog degas degum deice deify deign deism deist deity delay deled deles delft delhi delis dells delly delta
delve demit demob demon demos demur denim dense dents depot depth derat deray derby derma derms desex desks deter deuce
devas devil devon dewax dewed dexes dhole dhoti dhows dials diana diane diary diazo diced dicer dices dicey dicks dicky
dicot dicta didos didst diets dight digit diked diker dikes dildo dills dilly dimer dimes dimly dinar dined diner dines
dingo dings dingy dinky dints diode dippy direr dirge dirks dirts dirty disco discs dishy disks distr ditch dites ditto
ditty divan divas dived diver dives divot divvy dixie dixit dizzy djinn djins docks dodge dodgy dodos doers doest doeth
doffs doges dogey doggo doggy dogie dogma doily doing dojos dolce dolci doled doles dolls dolly dolor dolts domed domes
donee dongs donna donne donor donut dooms doors doozy doped doper dopes dopey doric doris dorms dormy dorsa dorsi dosed
doser doses doted doter dotes dotty doubt douce dough douse dover doves dowdy dowel dower downs downy dowry dowse doxie
doyen doyly dozed dozen dozer dozes drabs draft drags drain drake drama drams drank drape drats drave drawl drawn draws
drays dread dream drear dreck dregs dreks dress drest dribs dried drier dries drift drill drily drink drips dript drive
droit droll drone drool droop drops dropt dross drove drown drubs drugs druid drums drunk drupe dryad dryer dryly duads
duals dubio ducal ducat duces duchy ducks ducky ducts duddy dudes duels duets duffs duffy dukes dulls dully dulse dumbs
dummy dumps dumpy dunce dunes dungs dungy dunks duped duper dupes duple dural durns durra durrs durst durum dusks dusky
dusts dusty dutch dwarf dwell dwelt dyads dyers dying dykes dynes eager eagle eared earls early earns earth eased easel
easer eases easts eaten eater eaved eaves ebbed ebons ebony eclat ecole ecrus edema edgar edged edger edges edict edify
edith edits educe educt eerie egads egged egger egret egypt eider eidos eight eikon eject eking eland elans elate elbow
elder elect elegy elfin elide elite ellen elope elses elude elver elves elvis embar embay embed ember embow emcee emeer
emend emery emily emirs emits emmet emote empty enact enate ended ender endow endue enema enemy enfin enjoy ennui enrol
ensky ensue enter entre entry enure envoi envoy epees epics epoch epode epoxy epsom equal equip erase erect ergot erica
erode erose erred error eruct erupt essay esses ester estop etape ethel ether ethic ethos ethyl etnas etude euler evade
evans evens event evert every evict evils evoke ewers ewing exact exalt exams excel execs exert exile exist exits expel
expos expwy extol extra exude exult exurb exxon eyers eying eyrie eyrir fable faced facer faces facet facia facie facto
facts faddy faded fader fades faery fagot fails faint faire fairs fairy faith faits faked faker fakes fakir falls false
famed fames fancy fanes fangs fanny faqir farad farce farcy fards fared farer fares farms faros farts fasts fatal fated
fates fatly fatso fatty faugh fault fauna fauns faust fauve favor fawns fawny faxed faxes fazed fazes fears fease feast
feats feaze fecal feces feeds feels feign feint feist felix fella fells felly felon felts femme femur fence fends fenny
feoff feral fermi ferns ferny ferry fesse fetal fetas fetch feted fetes fetid fetor fetus feuds fever fewer feyer fezes
fiats fiber fibre fiche fichu fidel fides fidos fiefs field fiend fiery fifed fifer fifes fifth fifty fight filar filch
filed filer files filet filii fille fills filly films filmy filth final finch finds fined finer fines finis finks finns
finny fiord fired firer fires firma firms firry first firth fishy fists fitly fiver fives fixed fixer fixes fixup fizzy
fjord flabs flack flags flail flair flake flaky flame flams flamy flank flans flaps flare flash flask flats flaws flawy
flaxy flays fleas fleck fleer flees fleet flesh flews flick flied flier flies fling flint flips flirt flite flits float
flock floes flogs flood floor flops flora floss flour flout flown flows flubs flued flues fluff fluid fluke fluky flume
flump flung flunk fluor flush flute fluty flyby flyer foals foams foamy focal focus foehn foeti fogey foggy fogie foils
foins foist folds folia folic folio folks folly fonds fondu fonts foods fools foots footy foray force fords fores forge
forgo forks forky forma forms forte forth forts forty forum fossa fosse fouls found fount fours fovea fowls foxed foxes
foyer frags frail frame franc frank franz fraps frats fraud fraus frays freak freed freer frees freon frere fresh frets
freud friar fried frier fries frigs frill frisk frizz frock froes frogs frond front frosh frost froth frown froze frugs
fruit frump fryer fucks fudge fuels fugal fuggy fugit fugue fujis fulls fully fumed fumer fumes fumet fundi funds fungi
funks funky funny furls furor furry furze furzy fused fusee fusel fuses fusil fussy fusty fuzed fuzee fuzes fuzil fuzzy
gabby gable gabon gaels gaffe gaffs gaged gager gages gaily gains gaits galas galax gales galls gally galop gamba gamed
gamer games gamey gamic gamin gamma gamut ganef ganev gangs ganja gaols gaped gaper gapes gappy garbo garbs garde garth
gases gasps gassy gated gates gator gauds gaudy gauge gauls gaunt gauss gauze gauzy gavel gavot gawks gawky gayer gayly
gazed gazer gazes gears gecko gecks geeks geese gelds gelee gelid gelts gemmy genal genes genet genic genie genii genoa
genre gents genus geode geoid germs germy gesso geste gests getup geums ghana ghast ghats ghees ghost ghoul giant gibed
giber gibes giddy gifts gigas gigue gilds gills gilly gilts gimel gimps gimpy ginks ginny gipsy girds girls girly girns
giros girth girts gismo gists given giver gives givin gizmo glace glade glads glady gland glans glare glary glass glaze
glazy gleam glean gleba glebe glees glens glide glims glint gloam gloat globe globs glogg gloms gloom glops glory gloss
glove glows gloze glued gluer glues gluey gluts glyph gnarl gnars gnash gnats gnawn gnaws gnome goads goals goats gobos
godly goers gofer gogos going golds golem golfs golly gombo gonad goner gongs gonif gonof goods goody gooey goofs goofy
gooks gooky goons goony goops goose goosy gored gores gorge gorki gorse gorsy goths gouda gouge gourd gouts gouty gowns
goyim graal grabs grace grade grads graft grail grain gramp grams grana grand grant grape graph grapy grasp grass grata
grate grave gravy grays graze great grebe greco greed greek green greet greta greys grids grief grift grigs grill grime
grimm grimy grind grins griot gripe grips gript gripy grist grits groan groat grogs groin groom grope gross grosz grots
group grout grove growl grown grows grubs gruel gruff grump grunt guaco guano guard guars guava gucks guess guest guffs
guide guild guile guilt guiro guise gulch gulfs gulfy gulls gully gulps gulpy gumbo gummy gunks gunny guppy gurus gushy
gussy gusto gusts gusty gutsy gutta gutty guyed gypsy gyral gyred gyres gyros gyrus gyved gyves habit hacks hades hadji
hadst haets hafts hague haiku hails hairs hairy haiti hajis hajji hakes haled haler hales hallo halls halos halts halva
halve hammy hance hands handy hangs hanks hanky hanoi hants haole haply happy hards hardy hared harem hares harks harms
harps harpy harry harsh harts hasid hasps hasta haste hasty hatch hated hater hates haugh hauls haunt haute haven haver
haves havoc hawed hawks hawse haydn hayed hayer hayes hazed hazel hazer hazes hdqrs heads heady heals heaps heard hears
heart heath heats heave heavy hecks hedge hedgy heeds heels hefts hefty heigh heils heirs heist helen helio helix hello
hells helms helot helps helve heman hemps hempy hence henna henry hents herbs herby herds heres heron heros hertz hewed
hewer hexad hexed hexer hexes hexyl hicks hided hider hides highs hight hiked hiker hikes hills hilly hilts hindi hinds
hindu hinge hinny hints hippo hippy hired hirer hires hists hitch hived hives hoagy hoard hoary hobby hobos hocks hocus
hodad hoers hogan hoggs hoise hoist hokey hokum holds holed holer holes holey hollo holly holts homed homer homes homey
homos honan honda honed honer hones honey honks honky honor hooch hoods hooey hoofs hooka hooks hooky hoops hoots hoped
hoper hopes hopis horah horal horas horde horns horny horse horst horsy hosed hoses hosts hotel hotly hound houri hours
house hovel hover howdy howes howls hoyle hubby hucks huffs huffy huger hulas hulks hulky hullo hulls human humid humor
humph humps humpy humus hunch hunks hunky hunts hurls hurly huron hurry hurts husks husky hussy hutch huzza hydra hydro
hyena hying hymen hymns hyped hyper hypes hypos hyrax hyson iambi iambs ichor icier icily icing icker icons ictus idaho
ideal ideas idiom idiot idled idler idles idols idyll idyls igloo ignis ikons ileal ileum iliad ilium iller image imago
imams imbed imbue immix imped impel imper imply inane inapt inarm incas incog incur incus index india indol indow indue
inept inert infer infix infos infra ingle ingot inked inker inkle inlay inlet inned inner input inset instr intel inter
intra intro inure inurn iodin ionic iotas iowan iraqi irate irene iring irish irked irons irony isaac islam isled isles
islet issei issue istle italy itchy items ivied ivies ivory ixias jabot jacal jacks jacky jacob jaded jades jaggs jaggy
jails jakes jalap jambs james janes janet janus japan japed japer japes jason jatos jaunt javas jawed jazzy jeans jeeps
jeers jefes jehad jehus jells jelly jemmy jenny jerks jerky jerry jesse jests jesus jetty jewed jewel jewry jibed jiber
jibes jiffs jiffy jihad jills jilts jimmy jingo jinni jinns jived jives jnana jocko jocks joeys johns joins joint joist
joked joker jokes jolly jolts jolty jonah jones joram jorum jotty joule joust jowls jowly joyce joyed juans judas judge
judos juice juicy jujus juked jukes julep jumbo jumps jumpy junco junks junky junta junto juror justs jutes jutty juxta
kabob kadis kafir kafka kaiak kakas kakis kales kalif kalpa kames kanas kanji kaons kapok kappa kaput karat karen karma
karst karts kasha kathy kayak kayos kazoo keats kebab kebob kedge keefs keels keens keeps kefir kelps kelpy kelts kempt
kendo kenny kenos kenya kepis kerbs kerfs kerns kerry ketch keyed khaki khans khats kicks kicky kiddo kiddy kiefs kikes
kills kilns kilos kilts kilty kinds kines kings kinks kinky kiosk kiowa kirks kited kiter kites kiths kitty kivas kiwis
klans kleig klieg klutz knack knaps knave knead kneed kneel knees knell knelt knife knish knits knobs knock knoll knots
knout known knows knurl koala koans kodak kohls kolas kooks kooky kopek kophs kopje koran korea kotos kraal kraft krait
kraut krebs krill krona krone kudos kudus kudzu kulak kyats kyoto kyrie label labia labor laced lacer laces lacey lacks
laded laden lader lades ladle lager laird lairs laity laked laker lakes lamas lambs lamed lamer lames lamia lamps lanai
lance lands lanes lanky lapel lapin lapis lapps lapse larch lards lardy lares large largo larks larky larry larva lased
laser lases lasso lasts latch lated laten later latex lathe laths lathy latin laude lauds laugh laura lavas laved laver
laves lawed lawns lawny laxer laxly layed layer lazar lazed lazes leach leads leady leafs leafy leaks leaky leans leant
leaps leapt learn leary lease leash least leave ledge ledgy leech leeds leeks leers leery lefts lefty legal leger leggy
legit leman lemma lemon lemur lends lenin lense lento leone leper letch lethe letup levee level lever levin levis lewis
liana liars libel liber libra libre libya lichi licht licit licks lidar lidos liege liens liers lieut lifer lifts liger
light liked liken liker likes lilac lilly lilts limas limbo limbs limby limed limes limey limit limns limos limps linac
linda lindy lined linen liner lines liney lingo lings links linky linos lints linty linum lions lipid lippy liras lisle
lisps lists liszt liter lites lithe litho litre lived liven liver lives livid livre llama llano loach loads loafs loams
loamy loans loath lobar lobby lobed lobes lobos local lochs locks locos locus loden lodes lodge loess lofts lofty logan
loges loggy logia logic logos loins lolls lolly loner longs loofa loofs looks looms loons loony loops loopy loose loots
loped loper lopes loppy loran lords lores loris lorry loser loses lossy lotos lotto lotus lough louie louis loupe loups
lours loury louse lousy louts loved lover loves lowed lower lowly loxes loyal luaus lubes luces lucia lucid lucks lucky
lucre luffs luges lulls lulus lumen lumps lumpy lunar lunas lunch lunes lunet lunge lungs lunks lupin lupus lurch lured
lurer lures lurid lurks lusts lusty luted lutes luxes lycee lying lymph lynch lyres lyric lysed lyses lysin macaw maced
macer maces macho machs macks macle macro madam madly madre mafia mages magic magma magus maids mails maims maine mains
maist maize major maker makes malay males malls malta malts malty mamas mamba mambo mamie mamma mammy manas maned manes
mange mango mangy mania manic manly manna manor manos manse manta manus maori maple maqui march marcs mardi mares marge
maria marie marks marry marse marsh marts maser mashy masks mason massa masse massy masts match mated mater mates matey
maths matin matte matts matzo mauls mauve maven mavin maxim maxis mayan mayas maybe mayor mayst mazed mazel mazer mazes
meads meals mealy means meant meany meats meaty mecca mecum medal media medic meeds meets melba melds melee melon melts
memos mends menus meows merci mercy merer meres merge merit merry mesas meshy meson messy metal meted meter metes metre
metro mewed mewls mezzo miami miaou miaow miasm miaul micas micks micro midas middy midge midis midst miens miffs miffy
miggs might mikes milan milch miler miles milks milky mille mills milos mimed mimeo mimer mimes mimic mince mincy minds
mined miner mines mingy minim minis minks minny minor mints minty minus mired mires mirks mirky mirth mirvs misdo miser
misos missy mists misty miter mites mitre mitts mixed mixer mixes mixup moans moats mobil mocha mocks modal model modem
modes modus mogul moils moire moist molar molds moldy moles molls molly molto molts momma mommy monad monde mondo money
monks monos monte month mooch moods moody mooed moola moons moony moore moors moory moose moots moped moper mopes mopey
moral moray morel mores morns moron morph morse moses mosey mosks mossy mosts motel motes motet motey moths mothy motif
motor motto moues mould moult mound mount mourn mouse mousy mouth moved mover moves movie mowed mower moxas moxie mucks
mucky mucus muddy mudra muffs mufti muggs muggy mujik mulch mulct muled mules muley mulla mulls multi multo mumbo mumms
mummy mumps munch muons mural murex murks murky mused muser muses mushy music musks musky mussy musts musty muted muter
mutes mutts muzzy mylar mynah mynas myope myopy myrrh myths nabob nacre nadir naiad naifs nails naive naked named namer
names nance nancy nanny napes nappy narco narcs nares naris narks nasal nasty natal nates natty naval navel naves navvy
nazis neaps nears neath neats necks needs needy negro negus nehru neigh neons nepal nerds nerts nertz nerve nervy nests
netty never nevus newel newer newly newsy newts nexus nicer niche nicks niece nifty nighs night nihil nills nimbi nines
ninny ninon ninth nippy nisei niter nitre nitro nitty nixed nixes nixie nixon nobby nobel noble nobly nocks nodal noddy
nodes nodus noels noggs nohow noire noise noisy nolle nomad nonce nones nooks nooky noons noose norma norms norse north
nosed noses nosey notal notch noted noter notes notre nouns novae novas novel noway nubby nubia nuder nudes nudge nudie
nudum nukes nullo nulls numbs nurse nutty nylon nymph oaken oakum oared oases oasis oasts oaten oater oaths obeah obeli
obese obeys obits oboes obols occur ocean ocher ochre octad octal octet octyl oculi odder oddly odeon odium odors odour
ofays offal offed offer often ofter ogees ogham ogive ogled ogler ogles ogres ohing ohmic oiled oiler oinks okapi okays
okras olden older oldie oleos olios olive ollas ology omaha ombre omega omens omits onces onery onion onset oohed oomph
oozed oozes opals opens opera opine opium opted optic orals orang orate orbed orbit orcas order ordos oread organ orgic
oriel orion orlon orris ortho osage osaka oscar osier osmic ossea ossia ostia other otter ought ouija ounce ousel ousts
outdo outed outer outgo outre ouzel ouzos ovals ovary ovate ovens overs overt ovine ovoid ovolo ovule owing owlet owned
owner oxbow oxeye oxide oxlip oxter oyers ozone paced pacer paces packs pacta pacts paddy padre padri paean pagan paged
pages pails paine pains paint pairs paled paler pales palls pally palms palmy palps palsy pampa panda paned panel panes
panga pangs panic pansy pants panty papal papas papaw paper pappy papua paras parch pared parer pares paris parka parks
parry parse parte parti parts party parve paseo pasha passe pasta paste pasts pasty patch pated paten pater pates paths
patio patly patsy patty pause pavan paved paver paves pawed pawer pawky pawls pawns paxes payed payee payer peace peach
peaks peaky peals pearl pears peart pease peats peaty peavy pecan pecks pecky pedal pedes pedro peeks peels peens peeps
peers peery peeve peggy peins pekes pekin pekoe pelfs pelts penal pence pends penes penis penna penny pense peons peony
peppy pepsi perch perdu perdy peres peril peris perks perky perms perry pesky pesos pests petal peter petit petri petro
petty pewee pewit phage pharm phase phial phlox phone phono phons phony photo phren phyla piano picas picks picky picot
piece piers pieta piety piggy pigmy piked piker pikes pilaf pilar piled piles pills pilot pimas pimps pinch pined pines
piney pings pinko pinks pinky pinna pinon pinta pinto pints pinup pions pious piped piper pipes pipet pipit pique pirog
pitas pitch piths pithy piton pivot pixel pixes pixie pizza place plack plaid plain plait plane plank plans plant plash
plasm plate plato plats platy playa plays plaza plead pleas pleat plebe plebs plena plied plier plies plink plods plonk
plops plots plows ploys pluck plugs plumb plume plump plums plumy plunk plush pluto plyer poach pocks pocky podgy podia
poems poesy poets poilu point poise poked poker pokes pokey polar poled poler poles polio polis polit polka polls polyp
polys pomes pomps ponce ponds pones pooch poohs pools poops popes poppa poppy porch pored pores porgy porks porky porno
porns ports posed poser poses posit posse posts potsy potty pouch pouff poufs poult pound pours pouts pouty power poxed
poxes prams prana prank praos prate prats praus prawn prays preen preps press prest prexy preys price prick pricy pride
pried prier pries prigs prima prime primo primp prims prink print prior prise prism priss privy prize proas probe prods
proem profs progs prole proms prone prong proof props prose prosy proud prove prowl prows proxy prude prune pryer psalm
pseud pshaw psych pubes pubic pubis puces pucks pudgy puffs puffy puggy puked pukes pukka puled puler pules pulls pulps
pulpy pulse pumas pumps punch punks punky punny punts punty pupae pupal pupas pupil puppy puree purer purge purim purls
purrs purse pursy pushy pussy puton putts putty pygmy pylon pyres pyrex pyric pyxes pyxie pyxis qaids qatar qiana qophs
quack quads quaff quags quail quais quake quaky quale qualm quant quark quart quash quasi quays quean queen queer quell
quern query quest queue queys quick quids quiet quill quilt quint quips quipu quire quirk quirt quite quito quits quods
quoin quoit quota quote quoth qursh rabbi rabic rabid raced racer races racks radar radii radio radix radon rafts ragas
raged rages raggy raids rails rains rainy raise rajah rajas raked raker rakes rales rally ralph ramie ramps ranch rands
randy ranee range rangy ranis ranks rants raped raper rapes rapid rarer rased raser rases rasps raspy ratch rated rater
rates ratio ratty raved ravel raven raver raves rawer rawly rayed rayon razed razee razer razes razor reach react readd
reads ready realm reals reams reaps rearm rears reave rebbe rebec rebel rebid rebop rebus rebut recap recks recon recta
recti recto recur recut reded redes redid redip redly redos redox redry redux redye reeds reedy reefs reefy reeks reeky
reels reeve refed refer refit refix refly refry regal reges regia rehem reich reify reign reins rekey relax relay relet
relic relit reman remap remet remit remix renal rends renew renig rents reoil repay repel repin reply repro reran rerun
resaw resay resee reset resew resin resow rests retch retie retro retry reuse revel revue rewax rewed rewin rewon rexes
rheas rheum rhine rhino rhomb rhumb rhyme rhyta rials ribby riced ricer rices riche ricks rider rides ridge ridgy riels
rifer riffs rifle rifts right rigid rigor riled riles rills rimed rimes rinds rings rinks rinse riots ripen riper ripes
risen riser rises rishi risks risky risus rites ritzy rival rived riven river rives rivet riyal roach roads roams roans
roars roast robed robes robin roble robot rocks rocky rodeo roger rogue roils roily roles rolls roman romeo romps rondo
roods roofs rooks rooky rooms roomy roost roots rooty roped roper ropes rosed roses roshi rosin rotes rotor roues rouge
rough round rouse roust route routs roved rover roves rowan rowdy rowed rowel rower royal rubes ruble rucks ruddy ruder
ruers ruffs rugby ruing ruins ruled ruler rules rumba rummy rumor rumps runes rungs runic runny runts runty rupee rural
ruses rushy rusks russe rusts rusty ruths rutty saber sable sabot sabra sacks sacra sadhu sadly safer safes sagas sager
sages saggy sagos sahib saids sails saint saith sakes sakis salad salem sales sally salon salsa salts salty salve salvo
samba sambo samoa sands sandy saned saner sanes sanga sangh sanka santa sapid sapor sappy sarah saran saree sarge saris
sarod sassy satan sated sates satin satyr sauce saucy saudi sauls sault sauna saute saved saver saves savor savoy savvy
sawed sawer saxes saxon sayee sayer sayst scabs scads scags scald scale scalp scaly scamp scams scans scant scape scare
scarf scarp scars scary scats scene scent schmo schul schwa scion scoff scold scone scoop scoot scope score scorn scots
scott scour scout scowl scows scrag scram scrap scree screw scrim scrip scrod scrub scuba scuds scuff sculk scull sculp
scums scups scurf scuta scute scuts seals seams seamy sears seats sects sedan seder sedge sedgy sedum seeds seedy seeks
seels seems seeps seepy seers segno segos segue seige seine seism seize selfs sells semen semis sends senna senor sense
sensu senti seoul sepal sepia sepoy septa septs seral sered serer seres serfs serge serif serin serow serum serve servo
setae setal seton setup seven sever sewed sewer sexed sexes sexto sexts shack shade shads shady shaft shags shahs shake
shako shaky shale shall shalt shaly shame shams shank shape shard share shark sharp shave shawl shawm shawn shaws shays
sheaf shear sheds sheen sheep sheer sheet sheik shelf shell sheol sherd shewn shews shied shier shies shift shill shily
shims shine shins shiny ships shipt shire shirk shirr shirt shish shist shits shiva shive shivs shlep shoal shoat shock
shoed shoer shoes shoji shone shook shoos shoot shope shops shore shorn short shote shots shout shove shown shows showy
shred shrew shrub shrug shuck shuls shuns shunt shush shute shuts shyer shyly sibyl sicks sided sides sidle siege sieur
sieve sifts sighs sight sigil sigma signs sikhs silex silks silky sills silly silos silts silty silva simon simps since
sines sinew singe sings sinhs sinks sinus sioux sippy sired siree siren sires sirup sisal sissy sitar sited sites situp
situs sixes sixte sixth sixty sized sizer sizes skags skald skate skean skeet skein skews skids skied skier skies skiey
skiff skiis skill skimp skims skink skins skips skirl skirt skits skoal skuas skulk skull skunk skyed skyey slabs slack
slags slain slake slams slang slant slaps slash slate slats slaty slave slavs slaws slays sleds sleek sleep sleet slept
slews slice slick slide slier slily slime slims slimy sling slink slips slipt slits slobs sloes slogs sloop slope slops
slosh sloth slots slows slubs slued slues slugs slump slums slung slunk slurp slurs slush sluts slyer slyly smack small
smart smash smear smell smelt smile smirk smite smith smock smoke smoky smote smuts snack snafu snags snail snake snaky
snaps snare snark snarl sneak sneer snick snide sniff snipe snips snits snobs snood snoop snoot snore snort snots snout
snows snowy snubs snuck snuff snugs soaks soaps soapy soars soave sober socks sodas soddy sodom sofar sofas sofia softs
softy soggy soils solar soled soles solid solos solve somas sonar sonde sones songs sonic sonny sooey sooth soots sooty
sophs sophy sopor soppy sorel sorer sores sorry sorts sough souls sound soups soupy sours souse south sowed sower soyas
space spade spain spake spale spank spans spare spark spars spasm spate spats spawn spays speak spear speck specs speed
spell spelt spend spent sperm spews spica spice spick spics spicy spied spiel spier spies spiff spike spiky spill spilt
spine spins spiny spire spiry spite spits spitz splat splay split spoil spoke spoof spook spool spoon spoor spore sport
spots spout sprat spray spree sprig sprit spuds spued spues spume spumy spunk spurn spurs spurt sputa squab squad squat
squaw squib squid stabs stack staff stage stags stagy staid stain stair stake stale stalk stall stamp stand stank staph
stare stark stars start stash state stats stave stays stead steak steal steam steed steel steep steer stein stele stems
steno steps stere stern stets steve stews stick stied sties stiff stile still stilt stimy sting stink stint stirs stoas
stoat stock stogy stoic stoke stole stomp stone stony stood stool stoop stops stopt store stork storm story stoup stout
stove stows strap straw stray strep strew stria strip strop strum strut stubs stuck studs study stuff stump stung stunk
stuns stunt stupa stupe styed styes style styli stymy suave sucks sucre sudan sudor sudsy suede suers suets suety sugar
suing suite suits sulfa sulks sulky sully sumac summa sumos sumps sunny sunup super supes supra surds surer surfs surfy
surge surgy surly susan sutra sutta swabs swage swail swain swale swami swamp swang swank swans swaps sward swarm swart
swash swath swats sways swear sweat swede sweep sweet swell swept swift swigs swill swims swine swing swipe swirl swish
swiss swoon swoop swops sword swore sworn swung sylph synch syncs synod syren syria syrup tabby tabla table taboo tabor
tacet tachs tacit tacks tacky tacos tacts taels taffy taiga tails taint taken taker takes talcs taler tales talks talky
tally talon talus tamed tamer tames tammy tampa tamps tango tangs tangy tanka tanks tansy tanto taped taper tapes tapir
tarde tardo tardy tared tares tarns taros tarot tarps tarry tarsi tarts tasks taste tasty tatar tater tatoo tatty taunt
taupe tauts tawny taxed taxer taxes taxis tazza tazze teach teaks teals teams tears teary tease teats techy tecum teddy
teems teens teeny teeth telex tells telly tempi tempo temps tempt tench tends tenet tenon tenor tense tenth tents tenty
tepee tepid terce terms terne terns terra terre terry terse tesla tests testy tetra texan texas texts thane thank thats
thaws theft their theme thens there therm these theta thews thewy thick thief thigh thine thing think thins third thole
thong thorn thoro thorp those thous three threw thrip throb throe throw thrum thuds thugs thumb thump thyme thymi thymy
tiara tiber tibet tibia ticks tidal tided tides tiers tiffs tiger tight tikes tikis tilde tiled tiler tiles tills tilth
tilts timed timer times timid tinct tined tines tinge tings tinny tints tipis tippy tipsy tired tires tiros titan titer
tithe title titre titty tizzy toads toady toast today toddy toffs toffy tofts tofus togae togas toils tokay toked token
tokes tokyo tolls tombs tomes tommy tonal toned toner tones tongs tonic tonne tools tooth toots topaz toped toper topes
topic topos toque torah toras torch torcs tores torii toros torsi torso torte torts torus total toted totem toter totes
touch tough tours touts towed towel tower towns towny toxic toxin toyed toyer toyon toyos trace track tract trade trail
train trait tramp trams traps trapt trash trave trawl trays tread treat treed trees treks trend tress trets trews treys
triad trial tribe trice trick tried trier tries trill trims trine trios tripe trips trite trode trois troll tromp troop
trope troth trots trout trove trows troys truce truck trued truer trues trull truly trump trunk truss trust truth tryst
tsars tsked tsuba tubal tubas tubby tubed tuber tubes tucks tudor tufas tuffs tufts tufty tules tulip tulle tulsa tumid
tummy tumor tumps tunas tuned tuner tunes tunic tunis tunny tuque turbo turds turfs turfy turks turns turps tusks tutee
tutor tutti tutus tuxes twain twang twats tweak tweed tween tweet twerp twice twier twigs twill twine twins twiny twirl
twirp twist twits twixt tying tykes tyler typal typed types typic typos tyred tyres tyros tzars udder uglis ukase ulcer
ulnae ulnar ulnas ultra ulvas umbel umber umbra umiak umped unapt unarm unary unbar unbid unbox uncap uncle uncos uncut
under undid undue unfed unfit unfix ungot unhat unhip unify union unite units unity unlaw unlay unled unlet unlit unman
unmet unpeg unpen unpin unrig unrip unsay unset unsew unsex untie until unwed unwit unwon unzip upend upped upper upset
urban ureal ureas ureic urged urger urges urine ursae usage users usher using usual usurp usury uteri utero utile utter
uveal uveas uvula vacua vacuo vadis vagal vague vagus vales valet valid valor valse value valva valve vamps vaned vanes
vapid vapor vases vasts vasty vatic vault vaunt veals vealy vedic veeps veers veery vegan vegas veils veins veiny velar
velds veldt velum venal vends venin venom vents venue venus verbs verde verdi verge versa verse verso verve vests vetch
vexed vexer vexes vials viand vibes vicar viced vices vichy video viers views viewy vigil vigor viler villa villi vinal
vinas vinca vined vines vinic vinos vinyl viola viols viper viral vireo virgo virid virtu virus visas vised vises visit
visor vista vitae vital vitro vivid vivre vixen vizir vizor vocal voces vodka vogue voice voids voila voile voles volga
volta volts vomit voted voter votes vouch vowed vowel vower vroom vrouw vrows vuggs vuggy vughs vulgo vulva vying wacks
wacky waddy waded wader wades wadis wafer wafts waged wager wages wagon wahoo waifs wails wains waist waits waive waked
waken waker wakes waled waler wales walks walla walls wally waltz wands waned wanes wanly wants wards wared wares warks
warms warns warps warts warty washy wasps waspy waste wasts watch water watts waugh wauls waved waver waves wavey wawls
waxed waxen waxer waxes wayne weald weals weans wears weary weave webby weber wedge wedgy weeds weedy weeks weens weeny
weeps weepy weest wefts weigh weird weirs welch welds wells welsh welts wench wends wenny wests wetly whack whale whams
whang whaps wharf whats wheal wheat wheel whelk whelm whelp whens where whets whews wheys which whiff whigs while whims
whine whiny whips whipt whirl whirr whirs whish whisk whist white whits whity whizz whole whomp whoop whops whore whorl
whose whoso whump wicks widen wider wides widow width wield wierd wifed wifes wight wilco wilds wiled wiles wills willy
wilts wince winch winds windy wined wines winey wings wingy winks winos wiped wiper wipes wired wirer wires wised wiser
wises wishy wisps wispy wists witch withe withy witty wived wiver wives wizen wizes woads woald woful woken wolds wolfs
woman wombs womby women wonky wonts woods woody wooed wooer woofs wools wooly woops woosh woozy words wordy works world
worms wormy worry worse worst worth worts would wound woven wowed wrack wrang wraps wrapt wrath wreak wreck wrens wrest
wried wrier wries wring wrist write writs wrong wrote wroth wrung wryer wryly wurst xebec xenia xenic xenon xeric xerox
xviii xxiii xylan xylem xysts yacht yacks yahoo yamen yamun yanks yards yarer yarns yawed yawls yawns yawps yearn years
yeast yeggs yells yelps yemen yenta yerba yeses yetis yield yipes yodel yodhs yodle yogas yogee yoghs yogic yogin yogis
yoked yokel yokes yolks yolky yonis yores young yourn yours youse youth yowed yowie yowls yucca yukon yules yummy yurts
zaire zarfs zazen zeals zebra zebus zeins zeiss zendo zeros zests zesty zetas zilch zincs zincy zings zingy zinky zippy
zitis zloty zoeas zombi zonal zoned zoner zones zooid zooks zooms zoons zowie zulus zunis
'''.split()

if __name__ == '__main__':
    main()
