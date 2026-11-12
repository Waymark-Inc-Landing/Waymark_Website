"""The Oklahoma city pages, one English/Spanish pair per city.

tools/build-services.py turns each entry into a page with the same template as the
service pages. In-person sessions happen only in Shawnee, and every page says so:
the other cities are served by phone or video, or by the drive to Shawnee. Only add a
city when there is something true and specific to say about it.
"""

_STEP1 = {
    'en': ('FIRST', 'A free 15-minute call', 'You tell us what is happening. We tell you honestly whether we can help.'),
    'es': ('PRIMERO', 'Una llamada gratis de 15 minutos', 'Nos cuentan lo que está pasando. Les decimos con honestidad si podemos ayudar.'),
}
_STEP3 = {
    'en': ('AND THEN', 'A plan you both work', 'A clear structure with steps between sessions, built on Dr. Jim Talley\'s fifty years of work with couples.'),
    'es': ('Y LUEGO', 'Un plan que los dos trabajan', 'Una estructura clara, con pasos entre sesiones, apoyada en los cincuenta años de trabajo con parejas del Dr. Jim Talley.'),
}
_NOT_COUNSELING = {
    'en': ('Is this marriage counseling?', 'No. It is coaching: structured, practical work on your marriage. We are not licensed counselors or therapists, and if licensed care is what you need we will say so and help you find it.'),
    'es': ('¿Esto es consejería matrimonial?', 'No. Es coaching: trabajo práctico y estructurado sobre su matrimonio. No somos consejeros licenciados ni terapeutas, y si necesitan un profesional licenciado se lo diremos y les ayudaremos a buscarlo.'),
}


def _city(key, en_slug, es_slug, city, en, es):
    out = {'kind': 'city', 'city': city}
    for lang, slug, d in (('en', en_slug, en), ('es', es_slug, es)):
        if lang == 'en':
            d.update(
                slug=slug, name='Marriage Coaching in %s' % city, short='marriage coaching in %s' % city,
                title='Christian Marriage Coaching in %s, OK | Waymark Inc.' % city,
                eyebrow='Marriage coaching · %s, Oklahoma' % city,
                steps_h='How it works from %s' % city,
            )
        else:
            d.update(
                slug=slug, name='Coaching matrimonial en %s' % city, short='el coaching matrimonial en %s' % city,
                title='Coaching matrimonial cristiano en %s, OK | Waymark Inc.' % city,
                eyebrow='Coaching matrimonial · %s, Oklahoma' % city,
                steps_h='Cómo funciona desde %s' % city,
            )
        d['steps'] = [_STEP1[lang], d.pop('step2'), _STEP3[lang]]
        d['faq'] = d['faq'] + [_NOT_COUNSELING[lang]]
        out[lang] = d
    return out


CITIES = [
    _city('shawnee', 'marriage-coaching-shawnee-ok', 'coaching-matrimonial-shawnee-ok', 'Shawnee', {
        'desc': 'Faith-based marriage and couples coaching in Shawnee, Oklahoma. In-person sessions in town, or by phone or video, in English and Spanish. First 15-minute call free.',
        'h1': 'Christian marriage coaching, here in Shawnee.',
        'lead': 'Waymark Inc. is <strong>based in Shawnee, Oklahoma</strong>. Couples from Shawnee, Tecumseh, McLoud, Seminole and across Pottawatomie County can meet with us in person, or by phone or video when life makes the drive hard.',
        'for': [
            ('Couples in Shawnee and nearby', 'From Shawnee, Tecumseh, McLoud, Seminole or anywhere in Pottawatomie County, an in-person session is a short drive.'),
            ('Couples who want privacy', 'In a town where everyone knows everyone, what is said in a session stays there. A phone or video session from home is always an option.'),
            ('Spanish-speaking couples', 'Every session is available in Spanish or English, with the same people and the same process.'),
        ],
        'step2': ('THEN', 'Sessions in person or from home', 'Meet with us face to face in Shawnee, or by phone or video. You can change from one to the other as the weeks go.'),
        'faq': [
            ('Where do sessions take place in Shawnee?', 'In person in Shawnee, by appointment. When you book, we confirm the time and the place with you. Phone and video sessions are also available.'),
            ('Do you work with couples from the towns around Shawnee?', 'Yes. Tecumseh, McLoud, Seminole, Prague and the rest of Pottawatomie County are a short drive from us, and phone or video sessions are available too.'),
        ],
    }, {
        'desc': 'Coaching matrimonial y para parejas basado en la fe en Shawnee, Oklahoma. Sesiones en persona en la ciudad, o por teléfono o video, en español. Primera llamada de 15 minutos gratis.',
        'h1': 'Coaching matrimonial cristiano, aquí en Shawnee.',
        'lead': 'Waymark Inc. <strong>tiene su sede en Shawnee, Oklahoma</strong>. Parejas de Shawnee, Tecumseh, McLoud, Seminole y de todo el condado de Pottawatomie pueden reunirse con nosotros en persona, o por teléfono o video cuando el viaje se complica.',
        'for': [
            ('Parejas de Shawnee y sus alrededores', 'Desde Shawnee, Tecumseh, McLoud, Seminole o cualquier parte del condado de Pottawatomie, una sesión en persona queda a poca distancia.'),
            ('Parejas que quieren privacidad', 'En una ciudad donde todos se conocen, lo que se dice en una sesión se queda ahí. Una sesión por teléfono o video desde casa siempre es una opción.'),
            ('Parejas que prefieren el español', 'Todas las sesiones están disponibles en español o en inglés, con las mismas personas y el mismo proceso.'),
        ],
        'step2': ('DESPUÉS', 'Sesiones en persona o desde casa', 'Reúnanse con nosotros cara a cara en Shawnee, o por teléfono o video. Pueden cambiar de una forma a la otra con el paso de las semanas.'),
        'faq': [
            ('¿Dónde son las sesiones en Shawnee?', 'En persona en Shawnee, con cita. Al agendar, confirmamos con ustedes la hora y el lugar. También hay sesiones por teléfono y video.'),
            ('¿Trabajan con parejas de los pueblos alrededor de Shawnee?', 'Sí. Tecumseh, McLoud, Seminole, Prague y el resto del condado de Pottawatomie nos quedan a poca distancia, y también hay sesiones por teléfono o video.'),
        ],
    }),
    _city('okc', 'marriage-coaching-oklahoma-city', 'coaching-matrimonial-oklahoma-city', 'Oklahoma City', {
        'desc': 'Faith-based marriage coaching for Oklahoma City couples, by phone or video, or in person in Shawnee about 40 minutes east. English and Spanish. First 15-minute call free.',
        'h1': 'Christian marriage coaching for Oklahoma City couples.',
        'lead': 'Shawnee is <strong>about 40 minutes east of Oklahoma City</strong> on I-40. Couples from across the metro can meet with us by phone or video from home, or make the drive for an in-person session.',
        'for': [
            ('Couples across the metro', 'From Midwest City, Moore, Yukon, Mustang or downtown, a phone or video session starts wherever you are.'),
            ('Couples who want distance from home', 'Some couples would rather work on their marriage away from their own neighborhood and church. The drive to Shawnee gives you that.'),
            ('Spanish-speaking couples', 'Faith-based marriage coaching in Spanish can be hard to find. We offer every session in Spanish or English.'),
        ],
        'step2': ('THEN', 'Sessions by phone or video', 'One hour at a time, from wherever each of you is in the city. In-person sessions are in Shawnee if you prefer the drive.'),
        'faq': [
            ('Do you have an office in Oklahoma City?', 'No. Our in-person sessions are in Shawnee, about 40 minutes east on I-40. Oklahoma City couples can meet with us by phone or video.'),
            ('How do the phone and video sessions work?', 'Each session is an hour, by phone or video, with work for the two of you to do before the next one.'),
        ],
    }, {
        'desc': 'Coaching matrimonial basado en la fe para parejas de Oklahoma City, en español, por teléfono o video, o en persona en Shawnee, a unos 40 minutos. Primera llamada gratis.',
        'h1': 'Coaching matrimonial cristiano para parejas de Oklahoma City.',
        'lead': 'Shawnee queda <strong>a unos 40 minutos al este de Oklahoma City</strong> por la I-40. Parejas de toda el área metropolitana pueden reunirse con nosotros por teléfono o video desde casa, o hacer el viaje para una sesión en persona.',
        'for': [
            ('Parejas de toda el área metropolitana', 'Desde Midwest City, Moore, Yukon, Mustang o el centro, una sesión por teléfono o video empieza donde ustedes estén.'),
            ('Parejas que quieren distancia de casa', 'Algunas parejas prefieren trabajar en su matrimonio lejos de su propio vecindario y de su iglesia. El viaje a Shawnee les da eso.'),
            ('Parejas que prefieren el español', 'El coaching matrimonial basado en la fe y en español puede ser difícil de encontrar. Ofrecemos todas las sesiones en español o en inglés.'),
        ],
        'step2': ('DESPUÉS', 'Sesiones por teléfono o video', 'Una hora a la vez, desde donde esté cada uno en la ciudad. Las sesiones en persona son en Shawnee, si prefieren hacer el viaje.'),
        'faq': [
            ('¿Tienen oficina en Oklahoma City?', 'No. Nuestras sesiones en persona son en Shawnee, a unos 40 minutos al este por la I-40. Las parejas de Oklahoma City pueden reunirse con nosotros por teléfono o video.'),
            ('¿Cómo funcionan las sesiones por teléfono y video?', 'Cada sesión dura una hora, por teléfono o video, con trabajo para los dos antes de la siguiente.'),
        ],
    }),
    _city('norman', 'marriage-coaching-norman-ok', 'coaching-matrimonial-norman-ok', 'Norman', {
        'desc': 'Faith-based marriage and premarital coaching for couples in Norman, Oklahoma, by phone or video, or in person in Shawnee about 40 minutes away. English and Spanish.',
        'h1': 'Christian marriage coaching for couples in Norman.',
        'lead': 'Shawnee is <strong>about 40 minutes from Norman</strong> on Highway 9. Couples from Norman, Noble and Moore can meet with us by phone or video, or come to Shawnee for an in-person session.',
        'for': [
            ('Couples in Norman, Noble and Moore', 'A phone or video session fits into an evening at home, with no drive across the metro.'),
            ('University families', 'Students, staff and faculty carry full calendars. A session by phone or video is easier to keep than an office visit.'),
            ('Engaged couples', 'If a wedding is ahead of you, premarital guidance helps you begin in the right order, before the hard conversations become arguments.'),
        ],
        'step2': ('THEN', 'Sessions by phone or video', 'One hour at a time, from home in Norman. In-person sessions are in Shawnee, a straight drive east on Highway 9.'),
        'faq': [
            ('Do you have an office in Norman?', 'No. Our in-person sessions are in Shawnee, about 40 minutes away on Highway 9. Couples in Norman can meet with us by phone or video.'),
            ('Do you work with couples who are not married yet?', 'Yes. Premarital guidance is for dating and engaged couples who want to prepare for the marriage, not only for the wedding day.'),
        ],
    }, {
        'desc': 'Coaching matrimonial y prematrimonial basado en la fe para parejas de Norman, Oklahoma, en español, por teléfono o video, o en persona en Shawnee, a unos 40 minutos.',
        'h1': 'Coaching matrimonial cristiano para parejas de Norman.',
        'lead': 'Shawnee queda <strong>a unos 40 minutos de Norman</strong> por la carretera 9. Parejas de Norman, Noble y Moore pueden reunirse con nosotros por teléfono o video, o venir a Shawnee para una sesión en persona.',
        'for': [
            ('Parejas de Norman, Noble y Moore', 'Una sesión por teléfono o video cabe en una tarde en casa, sin cruzar el área metropolitana.'),
            ('Familias de la universidad', 'Estudiantes, personal y profesores tienen la agenda llena. Una sesión por teléfono o video es más fácil de cumplir que una visita a una oficina.'),
            ('Parejas comprometidas', 'Si tienen una boda por delante, la orientación prematrimonial les ayuda a comenzar en el orden correcto, antes de que las conversaciones difíciles se vuelvan discusiones.'),
        ],
        'step2': ('DESPUÉS', 'Sesiones por teléfono o video', 'Una hora a la vez, desde casa en Norman. Las sesiones en persona son en Shawnee, un viaje directo hacia el este por la carretera 9.'),
        'faq': [
            ('¿Tienen oficina en Norman?', 'No. Nuestras sesiones en persona son en Shawnee, a unos 40 minutos por la carretera 9. Las parejas de Norman pueden reunirse con nosotros por teléfono o video.'),
            ('¿Trabajan con parejas que todavía no están casadas?', 'Sí. La orientación prematrimonial es para novios y parejas comprometidas que quieren prepararse para el matrimonio, no solo para el día de la boda.'),
        ],
    }),
    _city('edmond', 'marriage-coaching-edmond-ok', 'coaching-matrimonial-edmond-ok', 'Edmond', {
        'desc': 'Faith-based marriage coaching for couples in Edmond, Oklahoma, by phone or video, or in person in Shawnee under an hour away. English and Spanish. First 15-minute call free.',
        'h1': 'Christian marriage coaching for couples in Edmond.',
        'lead': 'Shawnee is <strong>a little under an hour from Edmond</strong>. Couples from Edmond, Guthrie and north Oklahoma City can meet with us by phone or video, or make the drive for an in-person session.',
        'for': [
            ('Couples in Edmond and Guthrie', 'A phone or video session saves the drive across the metro and fits around work and school pickups.'),
            ('Couples with full calendars', 'When every evening already has something in it, an hour from home is the hour you can actually keep.'),
            ('Couples in ministry', 'If you lead in your church, it helps to talk with someone outside it. We are not part of your congregation or your denomination.'),
        ],
        'step2': ('THEN', 'Sessions by phone or video', 'One hour at a time, from home in Edmond. In-person sessions are in Shawnee for couples who want to sit down face to face.'),
        'faq': [
            ('Do you have an office in Edmond?', 'No. Our in-person sessions are in Shawnee, a little under an hour away. Couples in Edmond can meet with us by phone or video.'),
            ('Will anyone at our church know?', 'No. We do not share what is said in a session with anyone.'),
        ],
    }, {
        'desc': 'Coaching matrimonial basado en la fe para parejas de Edmond, Oklahoma, en español, por teléfono o video, o en persona en Shawnee, a menos de una hora. Primera llamada gratis.',
        'h1': 'Coaching matrimonial cristiano para parejas de Edmond.',
        'lead': 'Shawnee queda <strong>a poco menos de una hora de Edmond</strong>. Parejas de Edmond, Guthrie y el norte de Oklahoma City pueden reunirse con nosotros por teléfono o video, o hacer el viaje para una sesión en persona.',
        'for': [
            ('Parejas de Edmond y Guthrie', 'Una sesión por teléfono o video ahorra el viaje por el área metropolitana y se acomoda al trabajo y a la escuela de los hijos.'),
            ('Parejas con la agenda llena', 'Cuando cada tarde ya tiene algo, una hora desde casa es la hora que de verdad pueden cumplir.'),
            ('Parejas en el ministerio', 'Si ustedes lideran en su iglesia, ayuda hablar con alguien de fuera. No somos parte de su congregación ni de su denominación.'),
        ],
        'step2': ('DESPUÉS', 'Sesiones por teléfono o video', 'Una hora a la vez, desde casa en Edmond. Las sesiones en persona son en Shawnee, para las parejas que quieren sentarse cara a cara.'),
        'faq': [
            ('¿Tienen oficina en Edmond?', 'No. Nuestras sesiones en persona son en Shawnee, a poco menos de una hora. Las parejas de Edmond pueden reunirse con nosotros por teléfono o video.'),
            ('¿Alguien en nuestra iglesia se va a enterar?', 'No. No compartimos con nadie lo que se habla en una sesión.'),
        ],
    }),
    _city('tulsa', 'marriage-coaching-tulsa-ok', 'coaching-matrimonial-tulsa-ok', 'Tulsa', {
        'desc': 'Faith-based marriage coaching for couples in Tulsa, Oklahoma, by phone or video, in English and Spanish. Built on 50+ years of work with couples. First 15-minute call free.',
        'h1': 'Christian marriage coaching for couples in Tulsa.',
        'lead': 'Tulsa is <strong>about an hour and a half from Shawnee, where we are based</strong>, so couples from Tulsa, Broken Arrow, Owasso, Jenks and Bixby can meet with us by phone or video, with the same people and the same process as in person.',
        'for': [
            ('Couples across the Tulsa area', 'From Broken Arrow, Owasso, Jenks, Bixby or midtown, a session starts wherever the two of you are.'),
            ('Couples who live apart right now', 'If you are separated, each of you can join the same call from a different place.'),
            ('Spanish-speaking couples', 'Every session is available in Spanish or English, for Tulsa families who would rather do this work in their own language.'),
        ],
        'step2': ('THEN', 'Sessions by phone or video', 'One hour at a time, from home in Tulsa. If you ever want to meet face to face, in-person sessions are in Shawnee.'),
        'faq': [
            ('Do you have an office in Tulsa?', 'No. We are based in Shawnee, about an hour and a half away, so Tulsa couples can meet with us by phone or video.'),
            ('Does marriage coaching by video really work?', 'Yes. Most of our sessions happen this way. What matters is the structure and the work the two of you do between sessions.'),
        ],
    }, {
        'desc': 'Coaching matrimonial basado en la fe para parejas de Tulsa, Oklahoma, en español, por teléfono o video. Más de 50 años de trabajo con parejas. Primera llamada de 15 minutos gratis.',
        'h1': 'Coaching matrimonial cristiano para parejas de Tulsa.',
        'lead': 'Tulsa queda <strong>a una hora y media de Shawnee, donde tenemos nuestra sede</strong>, así que las parejas de Tulsa, Broken Arrow, Owasso, Jenks y Bixby pueden reunirse con nosotros por teléfono o video, con las mismas personas y el mismo proceso que en persona.',
        'for': [
            ('Parejas de toda el área de Tulsa', 'Desde Broken Arrow, Owasso, Jenks, Bixby o el centro, una sesión empieza donde estén los dos.'),
            ('Parejas que hoy viven separadas', 'Si están separados, cada uno puede unirse a la misma llamada desde un lugar distinto.'),
            ('Parejas que prefieren el español', 'Todas las sesiones están disponibles en español o en inglés, para las familias de Tulsa que prefieren hacer este trabajo en su propio idioma.'),
        ],
        'step2': ('DESPUÉS', 'Sesiones por teléfono o video', 'Una hora a la vez, desde casa en Tulsa. Si alguna vez quieren reunirse cara a cara, las sesiones en persona son en Shawnee.'),
        'faq': [
            ('¿Tienen oficina en Tulsa?', 'No. Nuestra sede está en Shawnee, a una hora y media, así que las parejas de Tulsa pueden reunirse con nosotros por teléfono o video.'),
            ('¿De verdad funciona el coaching matrimonial por video?', 'Sí. La mayoría de nuestras sesiones son así. Lo que importa es la estructura y el trabajo que los dos hacen entre sesiones.'),
        ],
    }),
]
