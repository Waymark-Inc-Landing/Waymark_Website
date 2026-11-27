#!/usr/bin/env python3
"""Build the journal articles in blog/ from the text below.

    python3 tools/build-articles.py

Each article is written once here, in English and Spanish, and comes out as a full page with
the shared header and footer (tools/shell.py), the look of the first devotional, and
BlogPosting structured data. Safe to run again: the pages are rewritten in place.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.waymarkinc.com'
STYLE_FROM = 'blog/your-worth-does-not-depend-on-your-performance.html'
DATE = '2026-11-27'
IMAGE = SITE + '/assets/about-mountains.jpg'

EXTRA_CSS = """
  /* ---- Journal articles ---- */
  article p a, .step a { color: var(--navy); text-decoration: none; border-bottom: 1px solid var(--gold); }
  article p a:hover, .step a:hover { color: var(--gold-deep); }
  .step p b { color: var(--ink); font-weight: 600; }
  .aside { font-size: 15.5px; color: var(--muted); border-top: 1px solid var(--line); margin-top: 44px; padding-top: 22px; }
"""

UI = {
    'en': dict(kicker='From the journal', by='Waymark Inc.', date='November 27, 2026',
               cta_q='Would you like someone to walk this with you?', cta_btn='Free 15-minute call',
               book='https://waymarkcoach.com/book/', locale='en_US',
               aside='We are coaches, not licensed counselors or therapists. We do not diagnose or treat mental health conditions.'),
    'es': dict(kicker='Del diario', by='Waymark Inc.', date='27 de noviembre de 2026',
               cta_q='¿Te gustaría que alguien caminara esto contigo?', cta_btn='Llamada gratis de 15 minutos',
               book='https://waymarkcoach.com/book/?clcm_lang=es', locale='es_US',
               aside='Somos coaches, no consejeros ni terapeutas con licencia. No hacemos diagnósticos ni tratamos condiciones de salud mental.'),
}

# Blocks: ('p', html) · ('h2', text) · ('steps', [html, ...]) · ('scripture', text, reference)
ARTICLES = [
    {
        'en': dict(
            slug='christian-marriage-coaching-vs-counseling',
            title='Christian Marriage Coaching vs. Counseling: The Difference',
            h1='Christian marriage coaching vs. counseling: what is the difference?',
            lead='Two kinds of help, two different jobs',
            desc='Marriage coaching and marriage counseling are not the same. Here is what each one does, how to tell which you need, and what Christian marriage coaching looks like at Waymark.',
            body=[
                ('scripture', 'Two are better than one… for if they fall, one will lift up the other.', 'Ecclesiastes 4:9–10'),
                ('p', 'Couples who are struggling often search for &ldquo;marriage counseling&rdquo; because it is the only name they know for getting help. Coaching is a different kind of help, and knowing the difference saves you time, money and disappointment.'),
                ('h2', 'What a licensed counselor does'),
                ('p', 'A marriage counselor or therapist holds a state license. That license allows them to diagnose and treat mental health conditions such as depression, anxiety, trauma and addiction. Much of their work looks at where a problem came from and how to treat it.'),
                ('h2', 'What a marriage coach does'),
                ('p', 'A coach does not diagnose or treat anything. Coaching is practical, structured work on the relationship itself: how the two of you talk, how you handle conflict, how trust is rebuilt, and what each of you will do before the next session. It looks mostly at where you are today and where you want to be.'),
                ('p', 'Christian marriage coaching adds one more thing. It stands on Scripture and on the conviction that God&rsquo;s plan for a broken marriage is restoration.'),
                ('h2', 'How to tell which one you need'),
                ('steps', [
                    '<b>See a licensed professional first</b> if either of you is dealing with a mental health condition, an addiction, thoughts of self-harm, or the effects of trauma.',
                    '<b>Get to safety first</b> if there is violence or you are afraid of your spouse. In the United States you can call the National Domestic Violence Hotline at 1-800-799-7233.',
                    '<b>Coaching fits</b> when the two of you are distant, stuck in the same argument, recovering from broken trust, or simply want a stronger marriage and a plan to build it.',
                    '<b>Sometimes it is both.</b> A couple can see a counselor for one need and work with a coach on the marriage at the same time.',
                ]),
                ('h2', 'What coaching looks like at Waymark'),
                ('p', 'We begin with a free 15-minute call. You tell us where things stand, and we tell you honestly whether coaching is the right fit. If what you need is a licensed professional, we will say so and help you look for one.'),
                ('p', 'After that, sessions are $100 each, by phone or video anywhere in the United States, in English or Spanish. In-person sessions are available in Shawnee, Oklahoma. One of you can start alone if the other is not ready.'),
                ('p', 'Read more about <a href="/online-christian-marriage-coaching/">online Christian marriage coaching</a> and <a href="/couples-coaching/">couples coaching</a>, or about <a href="/blog/how-to-rebuild-trust-in-a-marriage.html">how trust is rebuilt</a>.'),
            ]),
        'es': dict(
            slug='coaching-matrimonial-cristiano-o-consejeria',
            title='Coaching matrimonial cristiano o consejería: la diferencia',
            h1='Coaching matrimonial cristiano o consejería: ¿cuál es la diferencia?',
            lead='Dos tipos de ayuda, dos trabajos distintos',
            desc='El coaching matrimonial y la consejería matrimonial no son lo mismo. Aquí explicamos qué hace cada uno, cómo saber cuál necesitan y cómo es el coaching matrimonial cristiano en Waymark.',
            body=[
                ('scripture', 'Mejores son dos que uno… porque si caen, el uno levantará a su compañero.', 'Eclesiastés 4:9–10'),
                ('p', 'Muchas parejas que están pasando un momento difícil buscan &ldquo;consejería matrimonial&rdquo; porque es el único nombre que conocen para pedir ayuda. El coaching es otro tipo de ayuda, y conocer la diferencia ahorra tiempo, dinero y desilusiones.'),
                ('h2', 'Qué hace un consejero con licencia'),
                ('p', 'Un consejero o terapeuta matrimonial tiene una licencia del estado. Esa licencia le permite diagnosticar y tratar condiciones de salud mental como la depresión, la ansiedad, el trauma y las adicciones. Gran parte de su trabajo mira de dónde viene un problema y cómo tratarlo.'),
                ('h2', 'Qué hace un coach matrimonial'),
                ('p', 'Un coach no diagnostica ni trata nada. El coaching es trabajo práctico y estructurado sobre la relación misma: cómo se hablan, cómo manejan los conflictos, cómo se reconstruye la confianza y qué va a hacer cada uno antes de la próxima sesión. Mira sobre todo dónde están hoy y a dónde quieren llegar.'),
                ('p', 'El coaching matrimonial cristiano añade algo más. Se apoya en la Escritura y en la convicción de que el plan de Dios para un matrimonio roto es la restauración.'),
                ('h2', 'Cómo saber cuál necesitan'),
                ('steps', [
                    '<b>Busquen primero a un profesional con licencia</b> si alguno de los dos enfrenta una condición de salud mental, una adicción, pensamientos de hacerse daño o las secuelas de un trauma.',
                    '<b>Primero la seguridad</b> si hay violencia o tienes miedo de tu cónyuge. En Estados Unidos puedes llamar a la Línea Nacional contra la Violencia Doméstica al 1-800-799-7233; atienden en español.',
                    '<b>El coaching sirve</b> cuando están distantes, atrapados en la misma discusión, recuperándose de una confianza rota, o simplemente quieren un matrimonio más fuerte y un plan para construirlo.',
                    '<b>A veces son las dos cosas.</b> Una pareja puede ver a un consejero por una necesidad y trabajar el matrimonio con un coach al mismo tiempo.',
                ]),
                ('h2', 'Cómo es el coaching en Waymark'),
                ('p', 'Empezamos con una llamada gratis de 15 minutos. Ustedes nos cuentan cómo están las cosas y nosotros les decimos con honestidad si el coaching es lo indicado. Si lo que necesitan es un profesional con licencia, se lo diremos y les ayudaremos a buscarlo.'),
                ('p', 'Después, las sesiones cuestan $100 cada una, por teléfono o video en cualquier lugar de Estados Unidos, en español o inglés. También hay sesiones en persona en Shawnee, Oklahoma. Uno de los dos puede empezar solo si el otro todavía no está listo.'),
                ('p', 'Conozcan más sobre el <a href="/es/coaching-matrimonial-cristiano-en-linea/">coaching matrimonial cristiano en línea</a> y el <a href="/es/coaching-para-parejas/">coaching para parejas</a>, o sobre <a href="/blog/como-reconstruir-la-confianza-en-el-matrimonio.html">cómo se reconstruye la confianza</a>.'),
            ]),
    },
    {
        'en': dict(
            slug='how-to-rebuild-trust-in-a-marriage',
            title='How to Rebuild Trust in a Marriage: Six Honest Steps',
            h1='How to rebuild trust in a marriage',
            lead='Six honest steps, taken in order',
            desc='Trust in a marriage is rebuilt by actions repeated over time, not by one apology. Six honest steps for the spouse who broke trust and the spouse who was hurt, from a Christian view.',
            body=[
                ('scripture', 'Bear with one another and forgive one another… as the Lord has forgiven you.', 'Colossians 3:13'),
                ('p', 'When trust breaks in a marriage, both people usually want the same thing: for it to stop hurting. One wants to be believed again. The other wants to feel safe again. Neither happens because of a single conversation.'),
                ('p', 'Trust is rebuilt the way it was built the first time, by what a person does again and again. Here is the order we have seen work.'),
                ('h2', 'Six steps'),
                ('steps', [
                    '<b>Tell the whole truth, once.</b> Trust cannot grow on a partial story. Each new detail that surfaces later starts the clock over.',
                    '<b>End what broke it.</b> Whatever it was, a relationship, a habit, a hidden account, it has to stop completely and visibly.',
                    '<b>Take responsibility without &ldquo;but.&rdquo;</b> An apology that explains why the other person shares the blame is not yet an apology.',
                    '<b>Offer openness before it is asked for.</b> The one who broke trust volunteers where they are, who they are with and what they are spending. This is temporary, and it is what makes belief possible again.',
                    '<b>Give the hurt time.</b> The spouse who was hurt will ask the same questions more than once. Patient answers are part of the repair.',
                    '<b>Keep small promises.</b> Being home when you said you would be matters more than a grand gesture. Trust returns through ordinary days.',
                ]),
                ('h2', 'Forgiveness and trust are not the same thing'),
                ('p', 'Forgiveness is a decision one person makes before God, and it can be given right away. Trust is a response to evidence, and it takes time. A spouse can truly forgive and still need months before they feel safe. That is not a failure of faith.'),
                ('h2', 'When to ask for help'),
                ('p', 'Most couples cannot do this alone, because every conversation about it turns into the same fight. A third person keeps the conversation honest and moving. Dr. Jim Talley spent more than fifty years walking couples through this, and <a href="/dr-jim-talley/">his work</a> is the ground we stand on.'),
                ('p', 'If there is violence or you are afraid, safety comes before any of these steps. In the United States, call the National Domestic Violence Hotline at 1-800-799-7233.'),
                ('p', 'See how <a href="/marriage-restoration/">marriage restoration coaching</a> works, or read <a href="/blog/when-only-one-spouse-wants-to-save-the-marriage.html">what to do when only one of you wants to try</a>.'),
            ]),
        'es': dict(
            slug='como-reconstruir-la-confianza-en-el-matrimonio',
            title='Cómo reconstruir la confianza en el matrimonio: 6 pasos',
            h1='Cómo reconstruir la confianza en el matrimonio',
            lead='Seis pasos honestos, en orden',
            desc='La confianza en el matrimonio se reconstruye con acciones repetidas en el tiempo, no con una sola disculpa. Seis pasos honestos para quien rompió la confianza y para quien fue herido, desde una mirada cristiana.',
            body=[
                ('scripture', 'Sopórtense unos a otros y perdónense… así como el Señor los perdonó.', 'Colosenses 3:13'),
                ('p', 'Cuando la confianza se rompe en un matrimonio, los dos suelen querer lo mismo: que deje de doler. Uno quiere que le vuelvan a creer. El otro quiere volver a sentirse seguro. Ninguna de las dos cosas sucede con una sola conversación.'),
                ('p', 'La confianza se reconstruye igual que se construyó la primera vez: con lo que una persona hace una y otra vez. Este es el orden que hemos visto funcionar.'),
                ('h2', 'Seis pasos'),
                ('steps', [
                    '<b>Decir toda la verdad, una sola vez.</b> La confianza no crece sobre una historia a medias. Cada detalle nuevo que aparece después vuelve a poner el reloj en cero.',
                    '<b>Terminar con lo que la rompió.</b> Sea lo que sea, una relación, un hábito, una cuenta escondida, tiene que terminar por completo y de manera visible.',
                    '<b>Asumir la responsabilidad sin &ldquo;pero&rdquo;.</b> Una disculpa que explica por qué la otra persona también tiene la culpa todavía no es una disculpa.',
                    '<b>Ofrecer transparencia antes de que la pidan.</b> Quien rompió la confianza dice por su cuenta dónde está, con quién y en qué gasta. Es temporal, y es lo que permite volver a creer.',
                    '<b>Darle tiempo al dolor.</b> Quien fue herido va a hacer las mismas preguntas más de una vez. Responder con paciencia es parte de la reparación.',
                    '<b>Cumplir las promesas pequeñas.</b> Llegar a casa a la hora que dijiste vale más que un gran gesto. La confianza regresa en los días comunes.',
                ]),
                ('h2', 'Perdonar y confiar no son lo mismo'),
                ('p', 'El perdón es una decisión que una persona toma delante de Dios, y puede darse de inmediato. La confianza es una respuesta a la evidencia, y toma tiempo. Una persona puede perdonar de verdad y aun así necesitar meses para sentirse segura. Eso no es falta de fe.'),
                ('h2', 'Cuándo pedir ayuda'),
                ('p', 'La mayoría de las parejas no puede hacerlo sola, porque cada conversación sobre el tema termina en la misma pelea. Una tercera persona mantiene la conversación honesta y en movimiento. El Dr. Jim Talley dedicó más de cincuenta años a acompañar a parejas en esto, y <a href="/es/dr-jim-talley/">su obra</a> es la base de la nuestra.'),
                ('p', 'Si hay violencia o tienes miedo, la seguridad va antes que cualquiera de estos pasos. En Estados Unidos, llama a la Línea Nacional contra la Violencia Doméstica al 1-800-799-7233; atienden en español.'),
                ('p', 'Conoce cómo funciona la <a href="/es/restauracion-matrimonial/">restauración matrimonial</a>, o lee <a href="/blog/como-restaurar-mi-matrimonio-cuando-solo-yo-quiero.html">qué hacer cuando solo uno de los dos quiere intentarlo</a>.'),
            ]),
    },
    {
        'en': dict(
            slug='questions-to-ask-before-getting-engaged',
            title='12 Questions to Ask Before Getting Engaged | Christian Couples',
            h1='12 questions to ask before you get engaged',
            lead='Conversations worth having before the ring',
            desc='Twelve questions Christian couples should talk through before getting engaged: faith, family, money, conflict, pace and the future. With advice on what to do when an answer worries you.',
            body=[
                ('scripture', 'Which of you, wanting to build a tower, does not first sit down and count the cost?', 'Luke 14:28'),
                ('p', 'Most couples plan a wedding more carefully than they plan a marriage. The questions below are not a test to pass. They are conversations, and a couple who has had them walks into engagement with their eyes open.'),
                ('p', 'Take them a few at a time. Answer for yourself first, then listen.'),
                ('h2', 'Faith'),
                ('steps', [
                    'What does following Christ look like in your ordinary week, and what do you hope it will look like in our home?',
                    'Which church will we belong to, and how involved do we each expect to be?',
                ]),
                ('h2', 'Family'),
                ('steps', [
                    'What did your parents&rsquo; marriage teach you, both what to repeat and what to leave behind?',
                    'Do we want children? How many, how soon, and how would we raise them?',
                    'How much say will our families have in our decisions?',
                ]),
                ('h2', 'Money'),
                ('steps', [
                    'What do you owe, what do you earn, and how do you decide what to spend?',
                    'Will we share accounts, and who will keep track?',
                ]),
                ('h2', 'Conflict and trust'),
                ('steps', [
                    'When we disagree, what do you do: speak, go quiet, or leave the room? What do you need from me then?',
                    'Is there anything in your past that I should hear from you and not from someone else?',
                ]),
                ('h2', 'Pace and the future'),
                ('steps', [
                    'Are we moving at a pace that lets us really know each other? What boundaries will we keep until we marry?',
                    'Where do we want to live, and whose work comes first if we have to choose?',
                    'What would make you want to give up, and what would we do before it came to that?',
                ]),
                ('h2', 'When an answer worries you'),
                ('p', 'A hard answer is not a reason to end things. It is a reason to slow down and talk with someone who can help you both hear each other. Dr. Jim Talley wrote <em>Too Close, Too Soon</em> about exactly this: couples who move too fast skip the conversations that would have held the marriage up.'),
                ('p', 'Our <a href="/premarital-guidance/">Christian premarital coaching</a> walks dating and engaged couples through these questions, online, in English or Spanish. The first 15-minute call is free.'),
            ]),
        'es': dict(
            slug='preguntas-antes-de-comprometerse',
            title='12 preguntas antes de comprometerse | Parejas cristianas',
            h1='12 preguntas antes de comprometerse',
            lead='Conversaciones que vale la pena tener antes del anillo',
            desc='Doce preguntas que las parejas cristianas deberían conversar antes de comprometerse: fe, familia, dinero, conflictos, ritmo y futuro. Con consejos para cuando una respuesta les preocupa.',
            body=[
                ('scripture', '¿Quién de ustedes, queriendo edificar una torre, no se sienta primero y calcula los gastos?', 'Lucas 14:28'),
                ('p', 'La mayoría de las parejas planea la boda con más cuidado que el matrimonio. Las preguntas de abajo no son un examen que hay que aprobar. Son conversaciones, y una pareja que las ha tenido llega al compromiso con los ojos abiertos.'),
                ('p', 'Tómenlas de a pocas. Responde primero por ti, y después escucha.'),
                ('h2', 'La fe'),
                ('steps', [
                    '¿Cómo se ve seguir a Cristo en tu semana normal, y cómo esperas que se vea en nuestro hogar?',
                    '¿A qué iglesia vamos a pertenecer, y qué tan involucrado espera estar cada uno?',
                ]),
                ('h2', 'La familia'),
                ('steps', [
                    '¿Qué te enseñó el matrimonio de tus padres: qué quieres repetir y qué quieres dejar atrás?',
                    '¿Queremos tener hijos? ¿Cuántos, cuándo, y cómo los criaríamos?',
                    '¿Cuánta voz van a tener nuestras familias en nuestras decisiones?',
                ]),
                ('h2', 'El dinero'),
                ('steps', [
                    '¿Cuánto debes, cuánto ganas y cómo decides en qué gastar?',
                    '¿Vamos a compartir las cuentas, y quién va a llevar el control?',
                ]),
                ('h2', 'Los conflictos y la confianza'),
                ('steps', [
                    'Cuando no estamos de acuerdo, ¿qué haces: hablas, te callas o te vas? ¿Qué necesitas de mí en ese momento?',
                    '¿Hay algo de tu pasado que yo debería escuchar de ti y no de otra persona?',
                ]),
                ('h2', 'El ritmo y el futuro'),
                ('steps', [
                    '¿Vamos a un ritmo que nos permite conocernos de verdad? ¿Qué límites vamos a guardar hasta casarnos?',
                    '¿Dónde queremos vivir, y el trabajo de quién va primero si hay que elegir?',
                    '¿Qué te haría querer rendirte, y qué haríamos antes de llegar a ese punto?',
                ]),
                ('h2', 'Cuando una respuesta les preocupa'),
                ('p', 'Una respuesta difícil no es motivo para terminar. Es motivo para ir más despacio y hablar con alguien que les ayude a escucharse. El Dr. Jim Talley escribió <em>Too Close, Too Soon</em> (Demasiado cerca, demasiado pronto) justamente sobre esto: las parejas que avanzan demasiado rápido se saltan las conversaciones que habrían sostenido el matrimonio.'),
                ('p', 'Nuestra <a href="/es/orientacion-prematrimonial/">orientación prematrimonial cristiana</a> acompaña a novios y comprometidos por estas preguntas, en línea, en español o inglés. La primera llamada de 15 minutos es gratis.'),
            ]),
    },
    {
        'en': dict(
            slug='when-only-one-spouse-wants-to-save-the-marriage',
            title='When Only One Spouse Wants to Save the Marriage',
            h1='When only one of you wants to save the marriage',
            lead='What one person can do, and what one person cannot',
            desc='Your spouse has given up and you have not. What one person can honestly do to restore a marriage, what to stop doing, and where the limits are, from a Christian view.',
            body=[
                ('scripture', 'Let us not grow weary of doing good, for in due season we will reap, if we do not give up.', 'Galatians 6:9'),
                ('p', 'It is one of the loneliest places in a marriage: you still want it, and your husband or wife says they are done. You did not choose this alone, and you cannot fix it alone. But what you do next still matters a great deal.'),
                ('h2', 'What one person cannot do'),
                ('p', 'You cannot make another person stay, feel, or change. Pleading, pressure and promises made in a panic usually push a tired spouse further away. Accepting this limit is not giving up. It is where honest work begins.'),
                ('h2', 'What one person can do'),
                ('steps', [
                    '<b>Stop the pursuit.</b> Fewer long messages, fewer arguments about the relationship. Give room without going cold.',
                    '<b>Own your part, and only your part.</b> Name it plainly, without asking for anything back.',
                    '<b>Change something they can see.</b> Not a speech about changing. One real change, kept for weeks.',
                    '<b>Be steady.</b> Kind, calm and consistent at home, with the children and about money, even when nothing comes back.',
                    '<b>Do not carry it alone.</b> Pray, and let a pastor, a mature friend or a coach walk with you. Avoid people who only tell you what you want to hear.',
                    '<b>Leave the door open.</b> Say once, clearly, that you want the marriage and are willing to do the work. Then let your life say it.',
                ]),
                ('h2', 'How long?'),
                ('p', 'Nobody can promise you an outcome. Some marriages are restored after one person held steady for months. Others are not. What we can say is that a person who does this work comes out clearer, steadier and closer to God, whatever their spouse decides.'),
                ('h2', 'An important limit'),
                ('p', 'None of this means staying where you are in danger. If there is violence or you are afraid, get to safety first. In the United States, call the National Domestic Violence Hotline at 1-800-799-7233.'),
                ('h2', 'You can start alone'),
                ('p', 'Many of the people we coach begin by themselves, because their spouse is not ready. That is a good place to start. See <a href="/marriage-restoration/">marriage restoration coaching</a>, or read <a href="/blog/how-to-rebuild-trust-in-a-marriage.html">how trust is rebuilt</a>. If the marriage has already ended, there is a path for that too: <a href="/rebuilding-after-divorce/">rebuilding after divorce</a>.'),
            ]),
        'es': dict(
            slug='como-restaurar-mi-matrimonio-cuando-solo-yo-quiero',
            title='Cómo restaurar mi matrimonio cuando solo yo quiero',
            h1='Cómo restaurar mi matrimonio cuando solo yo quiero intentarlo',
            lead='Lo que una persona puede hacer, y lo que no',
            desc='Tu cónyuge se dio por vencido y tú no. Qué puede hacer honestamente una sola persona para restaurar su matrimonio, qué dejar de hacer y dónde están los límites, desde una mirada cristiana.',
            body=[
                ('scripture', 'No nos cansemos de hacer el bien, porque a su tiempo cosecharemos, si no nos damos por vencidos.', 'Gálatas 6:9'),
                ('p', 'Es uno de los lugares más solitarios de un matrimonio: tú todavía lo quieres, y tu esposo o tu esposa dice que ya no. No llegaste aquí solo, y no lo puedes arreglar solo. Pero lo que hagas ahora sigue importando mucho.'),
                ('h2', 'Lo que una sola persona no puede hacer'),
                ('p', 'No puedes obligar a otra persona a quedarse, a sentir o a cambiar. Las súplicas, la presión y las promesas hechas en un momento de pánico casi siempre alejan más a un cónyuge cansado. Aceptar este límite no es rendirse. Es donde empieza el trabajo honesto.'),
                ('h2', 'Lo que una sola persona sí puede hacer'),
                ('steps', [
                    '<b>Deja de perseguir.</b> Menos mensajes largos, menos discusiones sobre la relación. Da espacio sin volverte frío.',
                    '<b>Reconoce tu parte, y solo tu parte.</b> Dila con claridad, sin pedir nada a cambio.',
                    '<b>Cambia algo que se pueda ver.</b> No un discurso sobre cambiar. Un cambio real, sostenido por semanas.',
                    '<b>Sé constante.</b> Amable, tranquilo y firme en casa, con los hijos y con el dinero, aunque no recibas nada de vuelta.',
                    '<b>No lo cargues solo.</b> Ora, y deja que un pastor, un amigo maduro o un coach camine contigo. Evita a quienes solo te dicen lo que quieres oír.',
                    '<b>Deja la puerta abierta.</b> Di una vez, con claridad, que quieres el matrimonio y que estás dispuesto a hacer el trabajo. Después, deja que tu vida lo diga.',
                ]),
                ('h2', '¿Por cuánto tiempo?'),
                ('p', 'Nadie puede prometerte un resultado. Algunos matrimonios se restauran después de que una persona se mantuvo firme por meses. Otros no. Lo que sí podemos decir es que quien hace este trabajo sale con más claridad, más firmeza y más cerca de Dios, decida lo que decida su cónyuge.'),
                ('h2', 'Un límite importante'),
                ('p', 'Nada de esto significa quedarte donde corres peligro. Si hay violencia o tienes miedo, primero ponte a salvo. En Estados Unidos, llama a la Línea Nacional contra la Violencia Doméstica al 1-800-799-7233; atienden en español.'),
                ('h2', 'Puedes empezar solo'),
                ('p', 'Muchas de las personas que acompañamos empiezan solas, porque su cónyuge todavía no está listo. Es un buen lugar para comenzar. Conoce la <a href="/es/restauracion-matrimonial/">restauración matrimonial</a>, o lee <a href="/blog/como-reconstruir-la-confianza-en-el-matrimonio.html">cómo se reconstruye la confianza</a>. Si el matrimonio ya terminó, también hay un camino: <a href="/es/reconstruccion-tras-el-divorcio/">reconstrucción tras el divorcio</a>.'),
            ]),
    },
]


def rel(a):
    return 'blog/%s.html' % a['slug']


def render_body(blocks):
    out = []
    for b in blocks:
        if b[0] == 'p':
            out.append('    <p>%s</p>' % b[1])
        elif b[0] == 'h2':
            out.append('    <h2>%s</h2>' % b[1])
        elif b[0] == 'scripture':
            out.append('    <div class="scripture">\n      <p>&ldquo;%s&rdquo;</p>\n      <cite>%s</cite>\n    </div>' % (b[1], b[2]))
        elif b[0] == 'steps':
            rows = '\n'.join('      <div class="step"><span class="n" aria-hidden="true"></span><p>%s</p></div>' % s for s in b[1])
            out.append('    <div class="steps">\n%s\n    </div>' % rows)
        else:
            raise SystemExit('unknown block %r' % (b[0],))
    return '\n\n'.join(out)


def page(a, lang, other, css):
    ui = UI[lang]
    url = '%s/%s' % (SITE, rel(a))
    other_url = '%s/%s' % (SITE, rel(other))
    en_url, es_url = (url, other_url) if lang == 'en' else (other_url, url)
    esc = lambda t: html.escape(t, quote=True)
    ld = {
        '@context': 'https://schema.org', '@type': 'BlogPosting',
        'headline': a['h1'], 'description': a['desc'], 'inLanguage': lang,
        'author': {'@type': 'Organization', '@id': SITE + '/#organization', 'name': 'Waymark Inc.', 'url': SITE + '/'},
        'publisher': {'@type': 'Organization', '@id': SITE + '/#organization', 'name': 'Waymark Inc.', 'url': SITE + '/'},
        'mainEntityOfPage': url, 'image': IMAGE, 'datePublished': DATE, 'dateModified': DATE,
    }
    return '''<!DOCTYPE html>
<html lang="%(lang)s">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>%(title)s | Waymark Inc.</title>
<meta name="description" content="%(desc)s" />
<link rel="canonical" href="%(url)s" />
<link rel="alternate" hreflang="en" href="%(en_url)s" />
<link rel="alternate" hreflang="es" href="%(es_url)s" />
<link rel="alternate" hreflang="x-default" href="%(en_url)s" />
<meta property="og:type" content="article" />
<meta property="og:title" content="%(h1)s" />
<meta property="og:description" content="%(desc)s" />
<meta property="og:url" content="%(url)s" />
<meta property="og:image" content="%(image)s" />
<meta property="og:locale" content="%(locale)s" />
<link rel="icon" href="/favicon.ico" sizes="any" />
<link rel="icon" type="image/svg+xml" href="../assets/waymark-symbol.svg" />
<link rel="apple-touch-icon" href="../assets/apple-touch-icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Urbanist:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
<script type="application/ld+json">
%(ld)s
</script>
<style>%(css)s</style>
<!-- shell:head -->
%(head)s
<!-- /shell:head -->
</head>
<body>

<!-- shell:header -->
%(header)s
<!-- /shell:header -->

<section class="wm-hero wm-dark short">
  <div class="wm-hero-in">
    <span class="kicker">%(kicker)s</span>
    <h1>%(h1)s</h1>
    <p class="lead">%(lead)s</p>
    <p class="hero-sub"><strong>%(by)s</strong> · %(date)s</p>
  </div>
</section>

<main class="wm-main">
<article>
  <div class="wrap">
%(body)s

    <p class="aside">%(aside)s</p>
  </div>
</article>

<div class="cta">
  <p>%(cta_q)s</p>
  <a class="btn" href="%(book)s">%(cta_btn)s</a>
</div>

</main>

<!-- shell:footer -->
%(footer)s
<!-- /shell:footer -->

<script src="/assets/tag.js" defer></script>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(a['title']), desc=esc(a['desc']), url=url, en_url=en_url, es_url=es_url,
        h1=esc(a['h1']), image=IMAGE, locale=ui['locale'], ld=json.dumps(ld, ensure_ascii=False, indent=2),
        css=css, head=shell.HEAD_ASSETS, header=shell.header(lang, '/' + rel(other)),
        kicker=ui['kicker'], lead=esc(a['lead']), by=ui['by'], date=ui['date'], body=render_body(a['body']),
        aside=ui['aside'], cta_q=ui['cta_q'], cta_btn=ui['cta_btn'], book=ui['book'],
        footer=shell.footer(lang, '/' + rel(other)) + '\n' + shell.FOOT_SCRIPT,
    )


def main() -> int:
    src = open(os.path.join(ROOT, STYLE_FROM), encoding='utf-8').read()
    css = re.search(r'<style>(.*?)</style>', src, re.S).group(1).rstrip() + '\n' + EXTRA_CSS
    for pair in ARTICLES:
        for lang, other in (('en', 'es'), ('es', 'en')):
            a = pair[lang]
            path = os.path.join(ROOT, rel(a))
            open(path, 'w', encoding='utf-8').write(page(a, lang, pair[other], css))
            print('built', rel(a))
    return 0


if __name__ == '__main__':
    sys.exit(main())
