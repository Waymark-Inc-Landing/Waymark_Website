#!/usr/bin/env python3
"""Generate the service pages, one English/Spanish pair per service.

Run this after ANY change to the copy below or to the template:

    python3 tools/build-services.py

Every page is written from the SERVICES list and one template, so the sixteen pages
cannot drift apart. The header and footer come from tools/shell.py (styles in
assets/shell.css); the page sections are styled by assets/service.css. The homepage links to these
pages; tools/build-es.py carries the same English-to-Spanish path pairs (SERVICE_ES)
so the Spanish homepage links to the Spanish pages. Keep the two in step.
"""
import json
import os
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell  # noqa: E402  (tools/shell.py: the shared header and footer)
from cities import CITIES  # noqa: E402  (tools/cities.py: the Oklahoma city pages)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.waymarkinc.com'
ORG = SITE + '/#organization'

# ---------------------------------------------------------------------------
# Text shared by every page, per language
# ---------------------------------------------------------------------------
UI = {
    'en': {
        'home': '/', 'home_label': 'Waymark Inc. — Marking the way back',
        'other_lang': 'Español', 'other_code': 'es',
        'book': 'https://waymarkcoach.com/book/',
        'offer': 'Sessions are $100 each. <strong>The first 15-minute call is free</strong>, with no obligation.',
        'call': 'Call (405)&nbsp;822-8300', 'wa': 'Message us on WhatsApp', 'book_label': 'Free 15-minute call',
        'email_label': 'Email us',
        'wa_text': "Hello, I'd like to know more about {}.",
        'marks': ['In English and Spanish', 'By phone or video', 'Anywhere in the United States', 'In person in Shawnee, OK'],
        'team_alt': 'Jose and Paula Villalpando of Waymark Inc.',
        'team_cap': 'Jose and Paula Villalpando', 'team_sub': 'With you from the first call',
        'for_eyebrow': 'Is this you?', 'steps_eyebrow': 'How it works',
        'about_eyebrow': 'Who you will talk to', 'about_h': 'With you from the first call.',
        'team_role': 'Founders, Waymark Inc.',
        'faq_eyebrow': 'Before you begin', 'related_eyebrow': 'More from Waymark', 'cta_eyebrow': 'Wherever you are',
        'for_h': 'Who this is for', 'steps_h': 'Three steps, one honest direction', 'faq_h': 'Questions people ask first',
        'know_h': 'Good to know',
        'know': [
            ('What is said here stays here', 'We do not share what is said in a session with anyone.'),
            ('There is help paying for coaching', 'When money is the reason someone never calls, another family can cover part of the cost. Ask us about sponsored coaching.'),
            ('In person or from home', 'Most sessions happen by phone or video. In-person sessions are available in Shawnee, Oklahoma.'),
        ],
        'disclosure': 'We are coaches, not licensed counselors or therapists. We do not diagnose and we do not treat mental health conditions. If licensed care is what you need, we will say so plainly and help you find it.',
        'legacy': 'Waymark Inc. continues the work of <a href="/dr-jim-talley/">Dr. Jim Talley</a> (1942&ndash;2025), who spent more than fifty years sitting with couples at the worst moment of their marriage and telling them the truth: that the way back exists, and that it is walked one honest step at a time.',
        'related_h': 'Other ways we can walk with you',
        'areas_label': 'Marriage coaching in Oklahoma',
        'cta_h': 'There is a way back. Let us help you find it.',
        'cta_p': 'Start with one conversation, with no obligation. Tell us where you are and we will help you find the next marker on the road.',
        'foot_home': 'waymarkinc.com', 'crumb_home': 'Home',
        'callbar_call': 'Call', 'locale': 'en_US', 'locale_alt': 'es_US',
        'state': 'Oklahoma', 'country': 'United States',
    },
    'es': {
        'home': '/es/', 'home_label': 'Waymark Inc. — Marcando el camino de regreso',
        'other_lang': 'English', 'other_code': 'en',
        'book': 'https://waymarkcoach.com/book/?clcm_lang=es',
        'offer': 'Cada sesión cuesta $100. <strong>La primera llamada de 15 minutos es gratis</strong>, sin compromiso.',
        'call': 'Llama al (405)&nbsp;822-8300', 'wa': 'Escríbenos por WhatsApp', 'book_label': 'Llamada gratis de 15 minutos',
        'email_label': 'Escríbenos un correo',
        'wa_text': 'Hola, quisiera saber más sobre {}.',
        'marks': ['En español e inglés', 'Por teléfono o video', 'Todo Estados Unidos', 'En persona en Shawnee, OK'],
        'team_alt': 'José y Paula Villalpando, de Waymark Inc.',
        'team_cap': 'José y Paula Villalpando', 'team_sub': 'Contigo desde la primera llamada',
        'for_eyebrow': '¿Te suena conocido?', 'steps_eyebrow': 'Cómo funciona',
        'about_eyebrow': 'Con quién vas a hablar', 'about_h': 'Contigo desde la primera llamada.',
        'team_role': 'Fundadores de Waymark Inc.',
        'faq_eyebrow': 'Antes de comenzar', 'related_eyebrow': 'Más de Waymark', 'cta_eyebrow': 'Dondequiera que estés',
        'for_h': 'Para quién es', 'steps_h': 'Tres pasos, una dirección honesta', 'faq_h': 'Lo que la gente pregunta primero',
        'know_h': 'Bueno saberlo',
        'know': [
            ('Lo que se dice aquí, se queda aquí', 'No compartimos con nadie lo que se habla en una sesión.'),
            ('Hay ayuda para pagar el coaching', 'Cuando el dinero es la razón por la que alguien nunca llama, otra familia puede cubrir parte del costo. Pregúntanos por el coaching patrocinado.'),
            ('En persona o desde casa', 'La mayoría de las sesiones son por teléfono o video. También hay sesiones en persona en Shawnee, Oklahoma.'),
        ],
        'disclosure': 'Somos coaches. No somos consejeros licenciados ni terapeutas, no hacemos diagnósticos y no tratamos condiciones de salud mental. Si lo que necesitas es un profesional licenciado, te lo diremos con claridad y te ayudaremos a buscarlo.',
        'legacy': 'Waymark Inc. continúa el trabajo del <a href="/es/dr-jim-talley/">Dr. Jim Talley</a> (1942&ndash;2025), quien pasó más de cincuenta años sentado con parejas en el peor momento de su matrimonio, diciéndoles la verdad: que el camino de regreso existe y se recorre un paso honesto a la vez.',
        'related_h': 'Otras formas en que podemos acompañarte',
        'areas_label': 'Coaching matrimonial en Oklahoma',
        'cta_h': 'Hay un camino de regreso. Permítenos ayudarte a encontrarlo.',
        'cta_p': 'Comienza con una sola conversación, sin compromiso. Cuéntanos dónde estás y te ayudaremos a encontrar la siguiente señal en el camino.',
        'foot_home': 'waymarkinc.com/es', 'crumb_home': 'Inicio',
        'callbar_call': 'Llamar', 'locale': 'es_US', 'locale_alt': 'en_US',
        'state': 'Oklahoma', 'country': 'Estados Unidos',
    },
}

# ---------------------------------------------------------------------------
# The services. Each entry holds both languages so a pair is always edited together.
#   steps: (label, heading, text)   for: (heading, text)   faq: (question, answer)
# ---------------------------------------------------------------------------
SERVICES = [
    {
        'en': {
            'slug': 'couples-coaching', 'name': 'Couples Coaching', 'short': 'couples coaching',
            'title': 'Christian Couples Coaching | Online & in Shawnee, OK | Waymark Inc.',
            'desc': 'Faith-based coaching for couples in crisis, rebuilding after betrayal, or wanting to grow closer. By phone or video anywhere in the US, in English and Spanish. First 15-minute call free.',
            'eyebrow': 'Christian couples coaching',
            'h1': 'When the two of you are stuck, there is still a way forward.',
            'lead': 'Structured, <strong>faith-based coaching for couples</strong>: in crisis, rebuilding after a betrayal, or simply wanting to be closer than you are today. We meet you where you are. <strong>It is not therapy.</strong>',
            'for': [
                ('Couples in a hard season', 'The same argument keeps coming back, the distance keeps growing, and neither of you knows how to stop it.'),
                ('Couples rebuilding trust', 'After a betrayal or a long silence, you both want to stay but do not know how to begin again.'),
                ('Couples who want more', 'Nothing is broken, but you want a marriage that is growing instead of coasting.'),
            ],
            'steps': [
                ('FIRST', 'A conversation', 'You tell us where things stand today and what you want to change. We listen and name the next honest step.'),
                ('THEN', 'A plan with steps', 'A clear structure with work for the two of you between sessions, so progress does not depend on how the week went.'),
                ('AND THEN', 'Someone alongside', 'We meet regularly and adjust the plan to what is actually working for your marriage.'),
            ],
            'faq': [
                ('Is couples coaching the same as marriage counseling?', 'No. Coaching is structured, practical work on your relationship: a plan you follow session by session. We are not licensed counselors or therapists and we do not diagnose or treat mental health conditions.'),
                ('Can one of us start alone?', 'Yes. Sometimes only one person is ready to begin. That still helps, and it is a good place to start.'),
                ('Do we have to live in Oklahoma?', 'No. Most sessions happen by phone or video, so we work with couples anywhere in the United States. In-person sessions are available in Shawnee, OK.'),
            ],
        },
        'es': {
            'slug': 'coaching-para-parejas', 'name': 'Coaching para parejas', 'short': 'el coaching para parejas',
            'title': 'Coaching cristiano para parejas | En línea y en Shawnee, OK | Waymark Inc.',
            'desc': 'Coaching basado en la fe para parejas en crisis, que reconstruyen tras una traición o que quieren acercarse más. Por teléfono o video en todo Estados Unidos, en español. Primera llamada gratis.',
            'eyebrow': 'Coaching cristiano para parejas',
            'h1': 'Cuando los dos están atascados, todavía hay un camino.',
            'lead': '<strong>Coaching para parejas basado en la fe</strong>, con estructura: para parejas en crisis, que reconstruyen después de una traición o que simplemente quieren estar más cerca de lo que están hoy. Los encontramos donde están. <strong>No es terapia.</strong>',
            'for': [
                ('Parejas en una temporada difícil', 'La misma discusión regresa una y otra vez, la distancia crece y ninguno de los dos sabe cómo detenerla.'),
                ('Parejas que reconstruyen la confianza', 'Después de una traición o de un largo silencio, los dos quieren quedarse pero no saben cómo empezar de nuevo.'),
                ('Parejas que quieren más', 'Nada está roto, pero quieren un matrimonio que crezca en lugar de solo mantenerse.'),
            ],
            'steps': [
                ('PRIMERO', 'Una conversación', 'Nos cuentan dónde están hoy y qué quieren que cambie. Escuchamos y nombramos el siguiente paso honesto.'),
                ('DESPUÉS', 'Un plan con pasos', 'Una estructura clara, con trabajo para los dos entre sesiones, para que el avance no dependa de cómo estuvo la semana.'),
                ('Y LUEGO', 'Acompañamiento', 'Nos reunimos con regularidad y ajustamos el plan según lo que de verdad esté funcionando en su matrimonio.'),
            ],
            'faq': [
                ('¿El coaching para parejas es lo mismo que la consejería matrimonial?', 'No. El coaching es trabajo práctico y estructurado sobre la relación: un plan que se recorre sesión por sesión. No somos consejeros licenciados ni terapeutas, y no hacemos diagnósticos ni tratamos condiciones de salud mental.'),
                ('¿Puede empezar uno solo de los dos?', 'Sí. A veces solo una de las dos personas está lista para empezar. Eso también sirve, y es un buen lugar por donde comenzar.'),
                ('¿Tenemos que vivir en Oklahoma?', 'No. La mayoría de las sesiones son por teléfono o video, así que trabajamos con parejas en cualquier parte de Estados Unidos. También hay sesiones en persona en Shawnee, OK.'),
            ],
        },
    },
    {
        'en': {
            'slug': 'marriage-restoration', 'name': 'Marriage Restoration', 'short': 'marriage restoration',
            'title': 'Marriage Restoration Coaching for Couples in Crisis | Waymark Inc.',
            'desc': 'A guided, nine-session path for marriages on the brink of separation or divorce. Faith-based coaching built on Dr. Jim Talley\'s 50+ years of reconciliation work. Online, in English and Spanish.',
            'eyebrow': 'Marriage restoration',
            'h1': 'Separated, or close to it? No marriage is beyond repair.',
            'lead': 'An intensive, guided path for <strong>marriages on the brink</strong>: proven steps that move a couple from separation back toward a lasting covenant. It is more structured than general couples coaching, and both of you do the work.',
            'offer': 'Nine one-hour sessions, $100 per session. <strong>The first 15-minute call is free</strong>, with no obligation.',
            'for': [
                ('Couples who are separated', 'You live apart, or are about to, and at least one of you is not ready to call it finished.'),
                ('Couples facing divorce', 'The word has been said out loud, maybe papers have been filed, and you want to know if there is another way.'),
                ('Couples after a betrayal', 'Trust has broken and you need more than good intentions: you need an order to do things in.'),
            ],
            'steps': [
                ('FIRST', 'An honest look', 'A conversation about where the marriage really stands and whether both of you are willing to walk the path.'),
                ('THEN', 'Nine structured sessions', 'A set sequence of steps, with work between sessions, built on the reconciliation method Dr. Jim Talley taught for decades.'),
                ('AND THEN', 'A marriage that holds', 'Rebuilt trust, healthier boundaries, and the tools to keep walking after the sessions end.'),
            ],
            'faq': [
                ('What is marriage restoration?', 'An intensive, guided path for marriages on the brink: nine sessions of proven steps that move a couple from separation back toward a lasting covenant. It is more structured than general couples coaching.'),
                ('What if my spouse will not come?', 'Start with a conversation anyway. One person can begin, and we will tell you plainly what is and is not possible from there.'),
                ('Is this counseling or therapy?', 'No. It is coaching. We are not licensed counselors or therapists, and if licensed care is what your situation needs we will say so and help you find it.'),
            ],
        },
        'es': {
            'slug': 'restauracion-matrimonial', 'name': 'Restauración matrimonial', 'short': 'la restauración matrimonial',
            'title': 'Restauración matrimonial cristiana para matrimonios en crisis | Waymark Inc.',
            'desc': 'Un camino guiado de nueve sesiones para matrimonios al borde de la separación o el divorcio. Coaching basado en la fe, con más de 50 años de trabajo del Dr. Jim Talley. En línea y en español.',
            'eyebrow': 'Restauración matrimonial',
            'h1': '¿Separados, o cerca de estarlo? Ningún matrimonio está más allá de la reparación.',
            'lead': 'Un camino intensivo y guiado para <strong>matrimonios al borde de la ruptura</strong>: pasos comprobados que llevan a una pareja de la separación de regreso hacia un pacto duradero. Es más estructurado que el coaching general para parejas, y los dos hacen el trabajo.',
            'offer': 'Nueve sesiones de una hora, $100 por sesión. <strong>La primera llamada de 15 minutos es gratis</strong>, sin compromiso.',
            'for': [
                ('Parejas separadas', 'Viven aparte, o están por hacerlo, y al menos uno de los dos no está listo para darlo por terminado.'),
                ('Parejas frente al divorcio', 'La palabra ya se dijo en voz alta, quizá ya hay papeles, y quieren saber si existe otro camino.'),
                ('Parejas después de una traición', 'La confianza se rompió y hace falta más que buenas intenciones: hace falta un orden para hacer las cosas.'),
            ],
            'steps': [
                ('PRIMERO', 'Una mirada honesta', 'Una conversación sobre dónde está de verdad el matrimonio y si los dos están dispuestos a recorrer el camino.'),
                ('DESPUÉS', 'Nueve sesiones con estructura', 'Una secuencia definida de pasos, con trabajo entre sesiones, basada en el método de reconciliación que el Dr. Jim Talley enseñó durante décadas.'),
                ('Y LUEGO', 'Un matrimonio que se sostiene', 'Confianza reconstruida, límites más sanos y las herramientas para seguir caminando cuando las sesiones terminan.'),
            ],
            'faq': [
                ('¿Qué es la restauración matrimonial?', 'Un camino intensivo y guiado para matrimonios al borde de la ruptura: nueve sesiones de pasos comprobados que llevan a una pareja de la separación de regreso hacia un pacto duradero. Es más estructurado que el coaching general para parejas.'),
                ('¿Y si mi cónyuge no quiere venir?', 'Empieza de todos modos con una conversación. Una sola persona puede comenzar, y te diremos con claridad qué es posible y qué no desde ahí.'),
                ('¿Esto es consejería o terapia?', 'No. Es coaching. No somos consejeros licenciados ni terapeutas, y si tu situación necesita un profesional licenciado te lo diremos y te ayudaremos a buscarlo.'),
            ],
        },
    },
    {
        'en': {
            'slug': 'spiritual-direction', 'name': 'Spiritual Direction', 'short': 'spiritual direction',
            'title': 'Christian Spiritual Direction | Online & in Shawnee, OK | Waymark Inc.',
            'desc': 'Faith-centered guidance for the questions beneath the questions: purpose, forgiveness, identity and the road back to peace. One-on-one, by phone or video, in English and Spanish.',
            'eyebrow': 'Christian spiritual direction',
            'h1': 'For the questions beneath the questions.',
            'lead': '<strong>Faith-centered guidance</strong> for the things that are hard to say out loud: purpose, forgiveness, identity, and the road back to peace. One person, one conversation at a time.',
            'for': [
                ('When faith feels far away', 'You still believe, but prayer has gone quiet and you do not know who to tell.'),
                ('When you cannot forgive', 'Someone else, or yourself. You know what you are supposed to feel and you do not feel it.'),
                ('When you are at a crossroads', 'A decision about calling, family or direction, and you want to make it with clear eyes and an honest heart.'),
            ],
            'steps': [
                ('FIRST', 'A conversation', 'You say where you are, in your own words. Nothing has to be polished.'),
                ('THEN', 'Honest questions', 'We look at what is underneath, with Scripture and prayer as the ground we stand on.'),
                ('AND THEN', 'A next step', 'You leave each session with something concrete to practice before the next one.'),
            ],
            'faq': [
                ('What is spiritual direction?', 'Regular one-on-one conversations with someone who helps you pay attention to what God is doing in your life and respond to it honestly. It is guidance, not therapy.'),
                ('Do I need to belong to a particular church?', 'No. Our work is Christian and rooted in Scripture, and you are welcome wherever you are in your faith.'),
                ('Is it only for individuals?', 'Spiritual direction is usually one-on-one. If the question is about your marriage, couples coaching may be the better starting place, and we will tell you so.'),
            ],
        },
        'es': {
            'slug': 'direccion-espiritual', 'name': 'Dirección espiritual', 'short': 'la dirección espiritual',
            'title': 'Dirección espiritual cristiana en español | Waymark Inc.',
            'desc': 'Acompañamiento centrado en la fe para las preguntas más profundas: propósito, perdón, identidad y el regreso a la paz. Uno a uno, por teléfono o video, en español e inglés.',
            'eyebrow': 'Dirección espiritual cristiana',
            'h1': 'Para las preguntas que están debajo de las preguntas.',
            'lead': '<strong>Acompañamiento centrado en la fe</strong> para lo que cuesta decir en voz alta: propósito, perdón, identidad y el regreso a la paz. Una persona, una conversación a la vez.',
            'for': [
                ('Cuando la fe se siente lejos', 'Todavía crees, pero la oración se quedó en silencio y no sabes a quién contárselo.'),
                ('Cuando no puedes perdonar', 'A otra persona, o a ti. Sabes lo que deberías sentir y no lo sientes.'),
                ('Cuando estás en una encrucijada', 'Una decisión sobre tu llamado, tu familia o tu rumbo, y quieres tomarla con claridad y con un corazón honesto.'),
            ],
            'steps': [
                ('PRIMERO', 'Una conversación', 'Dices dónde estás, con tus propias palabras. Nada tiene que sonar bien.'),
                ('DESPUÉS', 'Preguntas honestas', 'Miramos lo que hay debajo, con la Escritura y la oración como el suelo donde nos paramos.'),
                ('Y LUEGO', 'Un siguiente paso', 'Sales de cada sesión con algo concreto para practicar antes de la siguiente.'),
            ],
            'faq': [
                ('¿Qué es la dirección espiritual?', 'Conversaciones regulares, uno a uno, con alguien que te ayuda a poner atención a lo que Dios está haciendo en tu vida y a responder con honestidad. Es acompañamiento, no terapia.'),
                ('¿Tengo que pertenecer a una iglesia en particular?', 'No. Nuestro trabajo es cristiano y está arraigado en la Escritura, y eres bienvenido estés donde estés en tu fe.'),
                ('¿Es solo para una persona?', 'La dirección espiritual suele ser uno a uno. Si la pregunta es sobre tu matrimonio, puede ser mejor empezar con el coaching para parejas, y te lo diremos.'),
            ],
        },
    },
    {
        'en': {
            'slug': 'coaching-for-ministers-and-leaders', 'name': 'Coaching for Ministers & Leaders', 'short': 'coaching for ministers and leaders',
            'title': 'Coaching for Pastors, Ministers & Leaders | Waymark Inc.',
            'desc': 'Confidential, faith-based coaching for pastors, ministers and leaders: guard your own marriage, family and calling while you serve others. By phone or video, in English and Spanish.',
            'eyebrow': 'Coaching for ministers and leaders',
            'h1': 'You carry everyone else. Who walks with you?',
            'lead': 'Confidential support for <strong>pastors, ministers, and leaders</strong> who pour into others: guarding your own marriage, your family, and your calling while you serve.',
            'for': [
                ('Pastors and ministry couples', 'The church gets your best hours and your marriage gets what is left. You both feel it.'),
                ('Leaders close to empty', 'You are still showing up, but there is less and less behind it, and there is no one inside the church you can safely tell.'),
                ('Leaders in a transition', 'A new role, a hard season in the congregation, or a decision about what comes next.'),
            ],
            'steps': [
                ('FIRST', 'A private conversation', 'Outside your church and your denomination. You can say what is true.'),
                ('THEN', 'A clear look', 'At your marriage, your family, your pace, and the boundaries that have worn thin.'),
                ('AND THEN', 'A sustainable way to serve', 'Concrete changes, worked on between sessions, so the calling does not cost you your home.'),
            ],
            'faq': [
                ('Will anyone in my church know?', 'No. We do not share what is said in a session with anyone, and we are not part of your church or denomination.'),
                ('Can my spouse join?', 'Yes. Many ministry leaders come as a couple, and some begin alone. Either works.'),
                ('Do you work with whole leadership teams?', 'We also work with churches and their leaders. Tell us what you are facing in the first conversation and we will say honestly whether we are the right help.'),
            ],
        },
        'es': {
            'slug': 'coaching-para-ministros-y-lideres', 'name': 'Coaching para ministros y líderes', 'short': 'el coaching para ministros y líderes',
            'title': 'Coaching para pastores, ministros y líderes | Waymark Inc.',
            'desc': 'Coaching confidencial y basado en la fe para pastores, ministros y líderes: cuida tu matrimonio, tu familia y tu llamado mientras sirves a otros. Por teléfono o video, en español.',
            'eyebrow': 'Coaching para ministros y líderes',
            'h1': 'Tú cargas con todos. ¿Quién camina contigo?',
            'lead': 'Apoyo confidencial para <strong>pastores, ministros y líderes</strong> que se entregan por los demás: cuida tu propio matrimonio, tu familia y tu llamado mientras sirves.',
            'for': [
                ('Pastores y parejas en el ministerio', 'La iglesia recibe tus mejores horas y tu matrimonio recibe lo que queda. Los dos lo sienten.'),
                ('Líderes casi vacíos', 'Sigues presentándote, pero cada vez hay menos detrás, y no hay nadie dentro de la iglesia a quien puedas contárselo con seguridad.'),
                ('Líderes en transición', 'Un nuevo cargo, una temporada difícil en la congregación o una decisión sobre lo que sigue.'),
            ],
            'steps': [
                ('PRIMERO', 'Una conversación privada', 'Fuera de tu iglesia y de tu denominación. Puedes decir lo que es verdad.'),
                ('DESPUÉS', 'Una mirada clara', 'A tu matrimonio, tu familia, tu ritmo y los límites que se han ido desgastando.'),
                ('Y LUEGO', 'Una forma sostenible de servir', 'Cambios concretos, trabajados entre sesiones, para que el llamado no te cueste tu hogar.'),
            ],
            'faq': [
                ('¿Alguien en mi iglesia se va a enterar?', 'No. No compartimos con nadie lo que se habla en una sesión, y no somos parte de tu iglesia ni de tu denominación.'),
                ('¿Puede participar mi cónyuge?', 'Sí. Muchos líderes vienen en pareja y otros empiezan solos. Las dos formas funcionan.'),
                ('¿Trabajan con equipos de liderazgo completos?', 'También trabajamos con iglesias y sus líderes. Cuéntanos lo que estás enfrentando en la primera conversación y te diremos con honestidad si somos la ayuda indicada.'),
            ],
        },
    },
    {
        'en': {
            'slug': 'premarital-guidance', 'name': 'Premarital Guidance', 'short': 'premarital guidance',
            'title': 'Christian Premarital Coaching & Guidance | Waymark Inc.',
            'desc': 'Faith-based premarital coaching for dating and engaged couples: build intimacy in the right order, on a foundation strong enough to last. Online, in English and Spanish.',
            'eyebrow': 'Christian premarital guidance',
            'h1': 'Begin in the right order.',
            'lead': 'Preparation for <strong>dating and engaged couples</strong> that helps you build intimacy on a foundation strong enough to last a lifetime. The questions are easier to ask before the wedding than after it.',
            'for': [
                ('Engaged couples', 'The date is set and you want to prepare for the marriage, not only for the day.'),
                ('Couples getting serious', 'You are talking about a future and want to know you are building it well.'),
                ('Couples marrying again', 'One or both of you has been married before, and you want this beginning to be different.'),
            ],
            'steps': [
                ('FIRST', 'Where you are', 'A conversation about your story so far and what each of you expects from marriage.'),
                ('THEN', 'The right pace', 'Dr. Jim Talley wrote <em>Too Close, Too Soon</em> about this: moving too fast keeps couples from building anything that holds.'),
                ('AND THEN', 'The hard conversations', 'Faith, family, money, conflict and boundaries, talked through before they become arguments.'),
            ],
            'faq': [
                ('When should we start?', 'As early as you are both willing. Couples who start before the engagement have more room to act on what they learn.'),
                ('Does this replace our church\'s premarital class?', 'It can stand alone or go alongside it. Tell us what your pastor requires and we will work with it.'),
                ('Can we do it if we live in different cities?', 'Yes. Sessions are by phone or video, so each of you can join from where you are.'),
            ],
        },
        'es': {
            'slug': 'orientacion-prematrimonial', 'name': 'Orientación prematrimonial', 'short': 'la orientación prematrimonial',
            'title': 'Orientación prematrimonial cristiana en español | Waymark Inc.',
            'desc': 'Coaching prematrimonial basado en la fe para novios y parejas comprometidas: construyan intimidad en el orden correcto, sobre un cimiento que dure. En línea y en español.',
            'eyebrow': 'Orientación prematrimonial cristiana',
            'h1': 'Comiencen en el orden correcto.',
            'lead': 'Preparación para <strong>novios y parejas comprometidas</strong> que les ayuda a construir intimidad sobre un cimiento lo suficientemente firme para toda la vida. Las preguntas son más fáciles de hacer antes de la boda que después.',
            'for': [
                ('Parejas comprometidas', 'La fecha ya está puesta y quieren prepararse para el matrimonio, no solo para el día.'),
                ('Parejas que van en serio', 'Ya hablan de un futuro y quieren saber que lo están construyendo bien.'),
                ('Parejas que se casan de nuevo', 'Uno de los dos, o ambos, ya estuvo casado, y quieren que este comienzo sea distinto.'),
            ],
            'steps': [
                ('PRIMERO', 'Dónde están', 'Una conversación sobre su historia hasta hoy y lo que cada uno espera del matrimonio.'),
                ('DESPUÉS', 'El ritmo correcto', 'El Dr. Jim Talley escribió <em>Too Close, Too Soon</em> sobre esto: avanzar demasiado rápido impide que una pareja construya algo que se sostenga.'),
                ('Y LUEGO', 'Las conversaciones difíciles', 'Fe, familia, dinero, conflicto y límites, hablados antes de que se vuelvan discusiones.'),
            ],
            'faq': [
                ('¿Cuándo deberíamos empezar?', 'Tan pronto como los dos estén dispuestos. Las parejas que empiezan antes del compromiso tienen más espacio para actuar sobre lo que aprenden.'),
                ('¿Esto reemplaza la clase prematrimonial de nuestra iglesia?', 'Puede ser independiente o ir a la par. Cuéntennos qué pide su pastor y trabajaremos con eso.'),
                ('¿Podemos hacerlo si vivimos en ciudades distintas?', 'Sí. Las sesiones son por teléfono o video, así que cada uno puede conectarse desde donde está.'),
            ],
        },
    },
    {
        'en': {
            'slug': 'rebuilding-after-divorce', 'name': 'Rebuilding After Divorce', 'short': 'rebuilding after divorce',
            'title': 'Christian Coaching After Divorce | Rebuilding Your Life | Waymark Inc.',
            'desc': 'Faith-based coaching for the season after a marriage ends: make sense of the loss, find your footing, and move forward without carrying the same wounds. Online, in English and Spanish.',
            'eyebrow': 'Rebuilding after divorce',
            'h1': 'The marriage ended. Your story did not.',
            'lead': 'For <strong>the season after a marriage ends</strong>: making sense of the loss, finding your footing again, and moving forward without carrying the same wounds into what comes next.',
            'for': [
                ('Recently divorced', 'The papers are signed and the house is quiet, and you do not know what the next year is supposed to look like.'),
                ('Divorced for years, still carrying it', 'Time has passed but the anger, guilt or grief has not, and it shows up in places you do not expect.'),
                ('Thinking about a new relationship', 'You want to understand what happened before you begin again.'),
            ],
            'steps': [
                ('FIRST', 'Telling the story', 'What happened, as you lived it, to someone who will not take sides or hurry you.'),
                ('THEN', 'Finding your footing', 'Grief, forgiveness, faith and daily life, one piece at a time, with work between sessions.'),
                ('AND THEN', 'Moving forward', 'Healthier boundaries and a clear sense of what you will and will not carry into what comes next.'),
            ],
            'faq': [
                ('Is this grief counseling?', 'No. It is coaching: practical, structured work on moving forward. We are not licensed counselors or therapists, and if licensed care is what you need we will say so and help you find it.'),
                ('Will you tell me I should have stayed?', 'No. We start from where you are today, with no judgment about how you got here.'),
                ('Is it too late if the divorce was years ago?', 'No. Many people come long after the divorce, when they notice the same wounds showing up again.'),
            ],
        },
        'es': {
            'slug': 'reconstruccion-tras-el-divorcio', 'name': 'Reconstrucción tras el divorcio', 'short': 'la reconstrucción tras el divorcio',
            'title': 'Coaching cristiano después del divorcio | Waymark Inc.',
            'desc': 'Coaching basado en la fe para la temporada después de que un matrimonio termina: dar sentido a la pérdida, recuperar el equilibrio y seguir adelante sin las mismas heridas. En línea y en español.',
            'eyebrow': 'Reconstrucción tras el divorcio',
            'h1': 'El matrimonio terminó. Tu historia no.',
            'lead': 'Para <strong>la temporada después de que un matrimonio termina</strong>: darle sentido a la pérdida, recuperar el equilibrio y seguir adelante sin llevar las mismas heridas a lo que viene.',
            'for': [
                ('Recién divorciados', 'Los papeles están firmados, la casa está en silencio y no sabes cómo se supone que sea el próximo año.'),
                ('Divorciados hace años, todavía con el peso', 'El tiempo pasó pero el enojo, la culpa o el duelo no, y aparecen donde menos lo esperas.'),
                ('Pensando en una nueva relación', 'Quieres entender lo que pasó antes de empezar de nuevo.'),
            ],
            'steps': [
                ('PRIMERO', 'Contar la historia', 'Lo que pasó, como tú lo viviste, a alguien que no va a tomar partido ni a apurarte.'),
                ('DESPUÉS', 'Recuperar el equilibrio', 'Duelo, perdón, fe y vida diaria, una parte a la vez, con trabajo entre sesiones.'),
                ('Y LUEGO', 'Seguir adelante', 'Límites más sanos y claridad sobre lo que vas a llevar, y lo que no, a lo que viene.'),
            ],
            'faq': [
                ('¿Esto es consejería de duelo?', 'No. Es coaching: trabajo práctico y estructurado para seguir adelante. No somos consejeros licenciados ni terapeutas, y si necesitas un profesional licenciado te lo diremos y te ayudaremos a buscarlo.'),
                ('¿Me van a decir que debí quedarme?', 'No. Empezamos desde donde estás hoy, sin juzgar cómo llegaste hasta aquí.'),
                ('¿Es demasiado tarde si el divorcio fue hace años?', 'No. Muchas personas llegan mucho después del divorcio, cuando notan que las mismas heridas vuelven a aparecer.'),
            ],
        },
    },
    {
        'kind': 'training',
        'en': {
            'slug': 'coach-training', 'name': 'Coach Training & Certification', 'short': 'coach training',
            'title': 'Christian Marriage Coach Training & Certification | Waymark Inc.',
            'desc': 'Training and certification in the Talley method for pastors, lay coaches and leaders who walk with couples. A structured curriculum, mentored cohorts and practical tools, in English and Spanish.',
            'eyebrow': 'For coaches and leaders',
            'h1': 'Learn to walk couples back to wholeness.',
            'lead': '<strong>Training and certification in the Talley method</strong>, structured for pastors, lay coaches, and leaders who want to make a lasting difference in the marriages around them.',
            'steps_h': 'What the training includes',
            'offer': 'Tell us about your ministry or practice and we will walk you through how the training works.',
            'for': [
                ('Pastors and ministry leaders', 'Couples already come to you in crisis, and you want more than instinct to offer them.'),
                ('Lay coaches and mentors', 'You walk with couples in your church or community and want a proven structure to follow.'),
                ('Coaches building a practice', 'You want a method you can carry into your own work and teach with confidence.'),
            ],
            'steps': [
                ('I', 'Certified curriculum', 'A structured, proven framework you can carry into your own ministry or practice, and teach with confidence.'),
                ('II', 'Mentored cohorts', 'Learn alongside other leaders, with direct guidance from seasoned coaches who have walked this road.'),
                ('III', 'Real-world tools', 'Practical resources for the hardest conversations the couples in your care will bring to you.'),
            ],
            'faq': [
                ('What is the Talley method?', 'The structured approach to reconciliation that Dr. Jim Talley developed and taught over more than fifty years of work with couples. Waymark Inc. carries it forward.'),
                ('Do I need to be a licensed counselor?', 'No. This is coach training. It does not make you a licensed counselor or therapist, and it teaches you when to refer a couple to licensed care.'),
                ('Is the training available in Spanish?', 'Yes. We train coaches and leaders in English and Spanish.'),
            ],
        },
        'es': {
            'slug': 'formacion-de-coaches', 'name': 'Formación y certificación de coaches', 'short': 'la formación de coaches',
            'title': 'Formación y certificación de coaches matrimoniales cristianos | Waymark Inc.',
            'desc': 'Formación y certificación en el método Talley para pastores, coaches y líderes que acompañan a parejas. Plan de estudios estructurado, grupos con mentoría y herramientas prácticas, en español.',
            'eyebrow': 'Para coaches y líderes',
            'h1': 'Aprende a acompañar a las parejas de regreso a la plenitud.',
            'lead': '<strong>Formación y certificación en el método Talley</strong>, estructurada para pastores, coaches y líderes que desean generar un impacto duradero en los matrimonios que los rodean.',
            'steps_h': 'Lo que incluye la formación',
            'offer': 'Cuéntanos sobre tu ministerio o tu práctica y te explicaremos cómo funciona la formación.',
            'for': [
                ('Pastores y líderes de ministerio', 'Las parejas ya llegan a ti en crisis, y quieres ofrecerles algo más que intuición.'),
                ('Coaches y mentores laicos', 'Acompañas a parejas en tu iglesia o tu comunidad y quieres una estructura comprobada que seguir.'),
                ('Coaches que construyen su práctica', 'Quieres un método que puedas llevar a tu propio trabajo y enseñar con confianza.'),
            ],
            'steps': [
                ('I', 'Plan de estudios certificado', 'Un marco estructurado y comprobado que puedes llevar a tu propio ministerio o práctica, y enseñar con confianza.'),
                ('II', 'Grupos con mentoría', 'Aprende junto a otros líderes, con la guía directa de coaches experimentados que han recorrido este camino.'),
                ('III', 'Herramientas reales', 'Recursos prácticos para las conversaciones más difíciles que las parejas a tu cuidado traerán a ti.'),
            ],
            'faq': [
                ('¿Qué es el método Talley?', 'El enfoque estructurado de reconciliación que el Dr. Jim Talley desarrolló y enseñó durante más de cincuenta años de trabajo con parejas. Waymark Inc. lo continúa.'),
                ('¿Necesito ser consejero licenciado?', 'No. Esta es una formación de coaches. No te convierte en consejero licenciado ni en terapeuta, y te enseña cuándo referir a una pareja a un profesional licenciado.'),
                ('¿La formación está disponible en español?', 'Sí. Formamos coaches y líderes en español e inglés.'),
            ],
        },
    },
    {
        'en': {
            'slug': 'online-christian-marriage-coaching', 'name': 'Online Christian Marriage Coaching', 'short': 'online marriage coaching',
            'title': 'Online Christian Marriage Coaching | Anywhere in the US | Waymark Inc.',
            'desc': 'Christian marriage coaching by phone or video, anywhere in the United States, in English and Spanish. Fifty years of work with couples behind every conversation. First 15-minute call free.',
            'eyebrow': 'Online Christian marriage coaching',
            'h1': 'Help for your marriage, wherever you live.',
            'lead': '<strong>Christian marriage coaching by phone or video</strong>, anywhere in the United States. The same people, the same process, and the same care as in person. Fifty years of work with couples stand behind every conversation.',
            'for': [
                ('Couples with no one nearby', 'There is no faith-based help for marriages where you live, or none you would trust with this.'),
                ('Couples who need privacy', 'In a small town or a close church, everyone knows everyone. A phone call from home stays at home.'),
                ('Couples with full schedules', 'Work, children and distance make an office visit impossible. A call does not need a commute.'),
            ],
            'steps': [
                ('FIRST', 'A free 15-minute call', 'You tell us what is happening. We tell you honestly whether we can help.'),
                ('THEN', 'Sessions by phone or video', 'One hour at a time, from wherever each of you is, with work to do between sessions.'),
                ('AND THEN', 'Someone to write to', 'Between sessions you can reach us by phone or WhatsApp when things get hard.'),
            ],
            'faq': [
                ('Does coaching by phone or video really work?', 'Yes. Most of our sessions happen this way. What matters is the structure and the work the two of you do between sessions.'),
                ('Which states do you serve?', 'All of them. We work with couples and individuals anywhere in the United States, and in person in Shawnee, Oklahoma.'),
                ('Do you offer sessions in Spanish?', 'Yes. Coaching is available in English and Spanish.'),
            ],
        },
        'es': {
            'slug': 'coaching-matrimonial-cristiano-en-linea', 'name': 'Coaching matrimonial cristiano en línea', 'short': 'el coaching matrimonial en línea',
            'title': 'Coaching matrimonial cristiano en línea, en español | Waymark Inc.',
            'desc': 'Coaching matrimonial cristiano en español, por teléfono o video, en cualquier parte de Estados Unidos. Cincuenta años de trabajo con parejas detrás de cada conversación. Primera llamada gratis.',
            'eyebrow': 'Coaching matrimonial cristiano en español',
            'h1': 'Ayuda para su matrimonio, vivan donde vivan.',
            'lead': '<strong>Coaching matrimonial cristiano en español</strong>, por teléfono o video, en cualquier parte de Estados Unidos. Las mismas personas, el mismo proceso y el mismo cuidado que en persona. Cincuenta años de trabajo con parejas respaldan cada conversación.',
            'for': [
                ('Parejas sin ayuda cerca', 'Donde viven no hay ayuda para matrimonios basada en la fe y en español, o ninguna a la que le confiarían esto.'),
                ('Parejas que necesitan privacidad', 'En un pueblo pequeño o una iglesia cercana todos se conocen. Una llamada desde casa se queda en casa.'),
                ('Parejas con poco tiempo', 'El trabajo, los hijos y la distancia hacen imposible ir a una oficina. Una llamada no necesita traslado.'),
            ],
            'steps': [
                ('PRIMERO', 'Una llamada gratis de 15 minutos', 'Nos cuentan lo que está pasando. Les decimos con honestidad si podemos ayudar.'),
                ('DESPUÉS', 'Sesiones por teléfono o video', 'Una hora a la vez, desde donde esté cada uno, con trabajo entre sesiones.'),
                ('Y LUEGO', 'Alguien a quien escribir', 'Entre sesiones pueden escribirnos o llamarnos por teléfono o WhatsApp cuando las cosas se compliquen.'),
            ],
            'faq': [
                ('¿De verdad funciona el coaching por teléfono o video?', 'Sí. La mayoría de nuestras sesiones son así. Lo que importa es la estructura y el trabajo que los dos hacen entre sesiones.'),
                ('¿En qué estados trabajan?', 'En todos. Acompañamos a parejas y personas en cualquier parte de Estados Unidos, y en persona en Shawnee, Oklahoma.'),
                ('¿Las sesiones son en español?', 'Sí. El coaching está disponible en español e inglés.'),
            ],
        },
    },
]


def path(lang: str, slug: str) -> str:
    return ('/es/' if lang == 'es' else '/') + slug + '/'


def esc_attr(s: str) -> str:
    return s.replace('&', '&amp;').replace('"', '&quot;')


def strip_tags(s: str) -> str:
    import re
    return re.sub(r'<[^>]+>', '', s)


def jsonld(lang: str, svc: dict, d: dict, url: str) -> str:
    ui = UI[lang]
    service = {
        '@type': 'Service', '@id': url + '#service',
        'name': d['name'], 'serviceType': d['name'], 'description': d['desc'],
        'url': url, 'inLanguage': lang,
        'provider': {'@type': 'LocalBusiness', '@id': ORG, 'name': 'Waymark Inc.', 'url': SITE + '/'},
        'areaServed': ([{'@type': 'City', 'name': svc['city']}] if svc.get('city') else [])
        + [{'@type': 'State', 'name': ui['state']}, {'@type': 'Country', 'name': ui['country']}],
        'availableLanguage': ['en', 'es'],
    }
    if svc.get('kind') != 'training':
        service['offers'] = {'@type': 'Offer', 'price': '100', 'priceCurrency': 'USD',
                             'description': strip_tags(d.get('offer', ui['offer']))}
    graph = [
        service,
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': ui['crumb_home'], 'item': SITE + ui['home']},
            {'@type': 'ListItem', 'position': 2, 'name': d['name'], 'item': url},
        ]},
        {'@type': 'FAQPage', 'inLanguage': lang, 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
            for q, a in d['faq']
        ]},
    ]
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=2)


def render(lang: str, svc: dict) -> str:
    ui, d = UI[lang], svc[lang]
    other = 'es' if lang == 'en' else 'en'
    url = SITE + path(lang, d['slug'])
    en_url = SITE + path('en', svc['en']['slug'])
    es_url = SITE + path('es', svc['es']['slug'])
    other_path = path(other, svc[other]['slug'])
    training = svc.get('kind') == 'training'
    wa = 'https://wa.me/14058228300?text=' + quote(ui['wa_text'].format(d['short']))
    mail = 'mailto:coaching@waymarkinc.com?subject=' + quote(d['name'])
    offer = d.get('offer', ui['offer'])

    if training:
        third = '<a class="wm-btn line" href="%s">%s</a>' % (mail, ui['email_label'])
    else:
        third = '<a class="wm-btn line" href="%s" target="_blank" rel="noopener" data-booking>%s</a>' % (ui['book'], ui['book_label'])
    actions = (
        '<a class="wm-btn gold" href="tel:14058228300">%s</a>\n'
        '      <a class="wm-btn wa" href="%s" target="_blank" rel="noopener">%s</a>\n'
        '      %s' % (ui['call'], wa, ui['wa'], third))

    marks = '\n      '.join('<span>%s</span>' % m for m in ui['marks'])
    items = '\n      '.join('<div class="item reveal"><h3>%s</h3><p>%s</p></div>' % c for c in d['for'])
    rows = '\n      '.join(
        '<div class="row reveal"><span class="n">%02d</span><div><span class="lbl">%s</span><h3>%s</h3></div><p>%s</p></div>'
        % (i + 1, s[0], s[1], s[2]) for i, s in enumerate(d['steps']))
    faq = '\n      '.join(
        '<details class="faq-item reveal"%s><summary>%s</summary><p>%s</p></details>'
        % (' open' if i == 0 else '', q, a) for i, (q, a) in enumerate(d['faq']))
    know = '\n        '.join('<li><b>%s</b>%s</li>' % k for k in ui['know'])
    related = '\n      '.join(
        '<a class="reveal" href="%s"><span>%s</span><i aria-hidden="true">→</i></a>'
        % (path(lang, s[lang]['slug']), s[lang]['name'].replace('&', '&amp;'))
        for s in SERVICES if s is not svc)
    areas = ' · '.join(
        '<a href="%s">%s</a>' % (path(lang, c[lang]['slug']), c['city'])
        for c in CITIES if c is not svc)
    steps_h = d.get('steps_h', ui['steps_h'])

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{d['title'].replace('&', '&amp;')}</title>
<meta name="description" content="{esc_attr(d['desc'])}" />
<link rel="canonical" href="{url}" />
<link rel="alternate" hreflang="en" href="{en_url}" />
<link rel="alternate" hreflang="es" href="{es_url}" />
<link rel="alternate" hreflang="x-default" href="{en_url}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Waymark Inc." />
<meta property="og:title" content="{esc_attr(d['name'])} | Waymark Inc." />
<meta property="og:description" content="{esc_attr(d['desc'])}" />
<meta property="og:url" content="{url}" />
<meta property="og:locale" content="{ui['locale']}" />
<meta property="og:locale:alternate" content="{ui['locale_alt']}" />
<meta property="og:image" content="{SITE}/assets/waymark-og-founders.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{esc_attr(ui['team_alt'])}" />
<link rel="icon" href="/favicon.ico" sizes="any" />
<link rel="icon" type="image/svg+xml" href="/assets/waymark-symbol.svg" />
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Urbanist:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
{shell.HEAD_ASSETS}
<link rel="stylesheet" href="/assets/service.css" />
<script type="application/ld+json">
{jsonld(lang, svc, d, url)}
</script>
<script src="/assets/tag.js"></script>
</head>
<body>

{shell.header(lang, other_path)}

<section class="wm-hero wm-dark">
  <div class="wm-hero-in">
    <span class="kicker">{d['eyebrow']}</span>
    <h1>{d['h1']}</h1>
    <p class="lead">{d['lead']}</p>
    <p class="offer">{offer}</p>
    <div class="actions">
      {actions}
    </div>
    <div class="marks">
      {marks}
    </div>
  </div>
</section>

<main class="wm-main">

<section class="block">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{ui['for_eyebrow']}</span>
      <h2>{ui['for_h']}</h2>
    </div>
    <div class="trio">
      {items}
    </div>
  </div>
</section>

<section class="dark wm-dark">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{ui['steps_eyebrow']}</span>
      <h2>{steps_h}</h2>
    </div>
    <div class="rows">
      {rows}
    </div>
  </div>
</section>

<section class="block about">
  <div class="wrap about-grid">
    <div class="portrait reveal">
      <div class="clip"><img src="/assets/waymark-founders.jpg" alt="{esc_attr(ui['team_alt'])}" width="1200" height="1800" loading="lazy" /></div>
    </div>
    <div class="about-body">
      <span class="eyebrow reveal">{ui['about_eyebrow']}</span>
      <h2 class="reveal">{ui['about_h']}</h2>
      <ul class="know reveal">
        {know}
      </ul>
      <p class="disclosure reveal">{ui['disclosure']}</p>
      <p class="legacy reveal">{ui['legacy']}</p>
      <div class="sign reveal"><div class="nm">{ui['team_cap']}</div><div class="rl">{ui['team_role']}</div></div>
    </div>
  </div>
</section>

<section class="block faq">
  <div class="wrap faq-grid">
    <div class="sec-head reveal">
      <span class="eyebrow">{ui['faq_eyebrow']}</span>
      <h2>{ui['faq_h']}</h2>
    </div>
    <div class="faq-list">
      {faq}
    </div>
  </div>
</section>

<section class="block related">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{ui['related_eyebrow']}</span>
      <h2>{ui['related_h']}</h2>
    </div>
    <nav class="related-list" aria-label="{esc_attr(ui['related_h'])}">
      {related}
    </nav>
    <p class="areas reveal"><span>{ui['areas_label']}</span> {areas}</p>
  </div>
</section>

<section class="contact wm-dark">
  <div class="wrap">
    <span class="eyebrow reveal">{ui['cta_eyebrow']}</span>
    <h2 class="reveal">{ui['cta_h']}</h2>
    <p class="sub reveal">{ui['cta_p']}</p>
    <div class="actions reveal">
      {actions}
    </div>
  </div>
</section>

</main>

{shell.footer(lang, other_path)}

<div class="callbar">
  <a href="tel:14058228300">{ui['callbar_call']}</a>
  <a href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
</div>

{shell.FOOT_SCRIPT}
<script src="/assets/lp.js"></script>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
'''


def main() -> int:
    n = 0
    for svc in SERVICES + CITIES:
        for lang in ('en', 'es'):
            d = svc[lang]
            for field, limit in (('title', 75), ('desc', 200)):
                if len(d[field]) > limit:
                    print('WARNING %s %s is %d characters' % (d['slug'], field, len(d[field])))
            out = os.path.join(ROOT, path(lang, d['slug']).strip('/'), 'index.html')
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, 'w', encoding='utf-8').write(render(lang, svc))
            n += 1
    print('wrote %d service and city pages' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
