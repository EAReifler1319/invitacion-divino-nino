"""Incorpora el contenido de la versión 'Niño Jesús (2)' manteniendo el diseño propio (se ejecutó una vez)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(p, encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)

# ---------------- CSS nuevo ----------------
rep('.card{content-visibility:auto;contain-intrinsic-size:auto 600px}',
'''.card{content-visibility:auto;contain-intrinsic-size:auto 600px}
/* Así será nuestra noche */
.noche{margin:30px 0 0;text-align:left}
.noche .tit{display:block;text-align:center;font-family:var(--script);font-size:clamp(34px,9.6vw,42px);color:#ffe3ea;line-height:1.1;margin-bottom:12px;text-shadow:0 2px 10px rgba(15,25,55,.35)}
.momento{display:flex;gap:14px;align-items:flex-start;margin:14px 0}
.momento .hora{flex:none;min-width:78px;padding:6px 10px;border-radius:12px;text-align:center;font-weight:700;font-size:17px;line-height:1.2;color:#3d5a8e;background:linear-gradient(145deg,#fbe6b0,#e9c46f)}
.momento p{margin:0;font-size:clamp(20px,5.8vw,22px)}
.ubic{display:inline-flex;align-items:center;gap:8px;margin-top:14px;padding:12px 20px;border-radius:999px;text-decoration:none;font-weight:700;font-size:19px;
  color:#3d5a8e;background:#fff;box-shadow:0 8px 20px rgba(15,25,60,.3);-webkit-tap-highlight-color:transparent}
.ubic svg{width:20px;height:20px}
.centro{text-align:center}
/* Actividad */
.insignia{display:table;margin:-4px auto 12px;padding:5px 16px;border-radius:999px;font-weight:700;font-size:16px;letter-spacing:.08em;text-transform:uppercase;
  color:#3d5a8e;background:linear-gradient(145deg,#fbe6b0,#e9c46f)}
.card .grande{font-size:clamp(22px,6.4vw,24px);text-align:center;margin:16px 0}
.card .nota{font-size:clamp(19px,5.4vw,21px);opacity:.9;text-align:center}
.ideas{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:16px 0 4px}
.ideas span{padding:8px 16px;border-radius:999px;font-weight:600;font-size:18px;background:rgba(255,255,255,.12);box-shadow:inset 0 0 0 1px rgba(249,220,146,.45)}
/* Dinámica de la foto */
.dinamica{margin-top:16px;padding:16px 18px;border-radius:18px;background:rgba(249,220,146,.12)}
.dinamica b{display:block;color:#f9dc92;font-size:21px;margin-bottom:6px}
.dinamica p{margin:0!important;font-size:19px!important}
.dinamica ul{margin:10px 0 0;padding-left:20px;font-size:19px;opacity:.92}
.dinamica li{margin:4px 0}
/* Compromiso */
.compromiso{display:flex;gap:14px;align-items:flex-start;margin:26px 0 0!important;padding:16px;border-radius:16px;background:rgba(255,255,255,.1);font-weight:600!important;font-size:20px!important;line-height:1.4;cursor:pointer}
.compromiso input{flex:none;width:26px;height:26px;margin:2px 0 0;accent-color:#e48fa6}
.compromiso.falta{box-shadow:0 0 0 3px rgba(255,160,180,.85)}
/* Pantalla final */
.hecho{text-align:center}
.hecho .gracias{font-family:var(--script);font-size:clamp(38px,11vw,48px);color:#ffe3ea;line-height:1.1;margin:6px 0 10px}
.hecho ol{text-align:left;margin:14px 0 0;padding-left:24px;font-size:20px}
.hecho li{margin:6px 0}''')

# ---------------- Portada ----------------
rep('''    <p class="navidad">¡Qué alegría! ¡Llegó la Navidad y quiero celebrarla contigo!</p>
    <p class="texto">Soy <span class="nombre">Emily Lamar</span>, la prioste de esta fiesta, y te invito con mucho cariño a compartir un momento de felicidad junto a las personas que más quiero.</p>
    <span class="orn o3 entra" aria-hidden="true" style="margin:26px auto 10px"></span>
    <p class="texto">Empezaremos con la <b>Santa Misa en San Cristóbal</b> y después nos reuniremos en el salón para compartir una <b>cena</b> y bonitos recuerdos juntos.</p>''',
'''    <p class="navidad">¡Qué felicidad! Llegó la Navidad y mi corazón quiere celebrarla contigo.</p>
    <p class="texto">Con mucho cariño, yo, <span class="nombre">Emily Lamar</span>, prioste de esta fiesta, te invito a vivir una noche llena de <b>luz, alegría y familia</b>.</p>
    <span class="orn o3 entra" aria-hidden="true" style="margin:26px auto 4px"></span>
    <div class="noche texto">
      <span class="tit">Así será nuestra noche</span>
      <div class="momento"><span class="hora">6:00<br>p. m.</span><p>Iniciamos con la <b>Santa Misa</b> en la <b>iglesia de San Cristóbal</b>.</p></div>
      <div class="momento"><span class="hora">Después</span><p>Nos reuniremos en un pequeño salón para compartir una <b>cena</b> llena de felicidad y bonitos recuerdos para todos.</p></div>
      <div class="centro"><a class="ubic" href="https://maps.app.goo.gl/yJQZnLQgtJXvJsDHA?g_st=ic" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="9.5" r="2.5" fill="currentColor"/></svg>
        Ver ubicación de la iglesia</a></div>
    </div>''')

# ---------------- Actividad ----------------
rep('''    <h2>Sé parte de una actividad</h2>
    <p>Te pido que traigas un <b>regalo de $1 por cada integrante de tu familia</b>. ¡Con ellos prepararé una sorpresa en la fiesta!</p>''',
'''    <h2>Sé parte de la actividad</h2>
    <span class="insignia">Es obligatoria</span>
    <p class="centro">Preparé una dinámica para divertirnos juntos y quiero que participes.</p>
    <p class="grande">Cada familia trae <b>un regalo de $1 por cada integrante</b></p>
    <p class="nota">Puede ser chistoso, lindo o creativo. Lo importante es que valga $1. Si son 5 personas, son 5 regalitos de $1.</p>
    <div class="ideas"><span>$1 de huevos</span><span>Un par de medias</span><span>Dulces</span><span>¡Sorpréndeme!</span></div>''')

# ---------------- Formulario ----------------
rep('''    <p class="intro">Solo completa estos 3 pasitos</p>''', '''    <div id="pasos">
    <p class="intro">Solo completa estos 3 pasitos y listo</p>''')
rep('placeholder="Ej.: Familia Lamar Álvaro"', 'placeholder="Ejemplo: Lamar Álvaro"')
rep('''      <p class="ayuda">Es obligatoria: ¡te tengo grandes sorpresas y tú eres parte de ellas!</p>
''', '')
rep('''      <input type="file" id="pic" accept="image/*" class="oculto">
    </div>

    <button type="button" class="btn" id="send">¡Confirmo mi asistencia!</button>
    <div id="msg" class="ok"></div>''',
'''      <input type="file" id="pic" accept="image/*" class="oculto">
      <div class="dinamica">
        <b>Tu foto es parte de una dinámica en familia</b>
        <p>Con ella prepararé algo especial para esa noche, y cada familia tendrá su momento para brillar. ¡Será muy divertido y lleno de sorpresas!</p>
        <ul>
          <li>Que salgan todos los que vienen a la fiesta</li>
          <li>Con buena luz y de frente</li>
          <li>¡Con sonrisas o una pose divertida!</li>
        </ul>
      </div>
    </div>

    <label class="compromiso" id="comp"><input type="checkbox" id="agree"><span>Me comprometo a traer un regalo de $1 por cada integrante de mi familia.</span></label>

    <button type="button" class="btn" id="send">¡Confirmo mi asistencia!</button>
    <div id="msg" class="ok" role="alert"></div>
    </div>

    <div class="hecho" id="hecho" hidden>
      <p class="gracias">¡Gracias, <span id="h-fam"></span>!</p>
      <p>Anoté <b id="h-n"></b>. Falta un último paso para que yo reciba tu confirmación:</p>
      <ol>
        <li>Toca el botón para enviarme el mensaje por WhatsApp.</li>
        <li>Si la foto no se adjunta sola, agrégala con el clip y envíala.</li>
      </ol>
      <button type="button" class="btn" id="wa">Enviar por WhatsApp</button>
    </div>''')

# ---------------- JS ----------------
rep('''/* Número de WhatsApp de la prioste (con código de país, sin + ni espacios). Ej.: 593991234567 */
const WHATSAPP='';''', '''/* Número de WhatsApp de Emily (con código de país, sin + ni espacios) */
const WHATSAPP='593995628433';''')
rep('''$('fam').oninput=()=>$('fam').classList.remove('falta');
async function porWhatsApp(fam){
  const texto='¡Hola, Emily! Confirmamos asistencia a la Fiesta del Divino Niño del 24 de diciembre. Familia: '+fam+'. Vamos '+n+' '+(n==1?'persona':'personas')+'.';
  const f=$('pic').files[0];
  /* En el celular: compartir texto + foto juntos (WhatsApp, etc.) */
  try{
    if(f&&navigator.canShare&&navigator.canShare({files:[f]})){
      await navigator.share({text:texto,files:[f]});
      aviso('¡Gracias, '+fam+'! Los espero con mucho cariño.','bien');petalos(40,true);return;
    }
  }catch(e){if(e&&e.name==='AbortError')return}
  const url='https://wa.me/'+WHATSAPP+'?text='+encodeURIComponent(texto+' Te envío la foto de nuestra familia.');
  const m=$('msg');m.className='ok';
  m.innerHTML='<p style="margin:0 0 4px">Último paso: envía tu confirmación por WhatsApp y <b>adjunta ahí la foto</b>.</p><a class="btn alt" target="_blank" rel="noopener" href="'+url+'">Enviar por WhatsApp</a>';
}''',
'''$('fam').oninput=()=>$('fam').classList.remove('falta');
$('agree').onchange=()=>$('comp').classList.remove('falta');
let famConf='';
function mensaje(){
  return '¡Hola, Emily! Confirmo mi asistencia a la Fiesta del Divino Niño\\nFamilia: '+famConf+'\\nPersonas: '+n+'\\nRegalos de $1 que traeremos: '+n+'\\n(Te envío la foto de mi familia)';
}
/* Enviar: en el celular comparte mensaje + foto juntos; si no se puede, abre el chat de WhatsApp */
$('wa').onclick=async()=>{
  const f=$('pic').files[0];
  try{
    if(f&&navigator.canShare&&navigator.canShare({files:[f]})){
      await navigator.share({text:mensaje(),files:[f]});petalos(40,true);return;
    }
  }catch(e){if(e&&e.name==='AbortError')return}
  window.open('https://wa.me/'+WHATSAPP+'?text='+encodeURIComponent(mensaje()),'_blank','noopener');
};
function terminar(fam){
  famConf=fam;
  $('h-fam').textContent=fam;$('h-n').textContent=n+(n==1?' persona':' personas');
  $('pasos').hidden=true;$('hecho').hidden=false;
  $('rsvp').scrollIntoView({behavior:'smooth',block:'start'});petalos(30,true);
}''')
rep('''  if(!$('pic').files[0]){aviso('Falta el paso 3: elige la foto de tu familia.','error');$('subir').classList.add('falta');$('subir').scrollIntoView({behavior:'smooth',block:'center'});return}
  if(!db||!me||!assets){porWhatsApp(fam);return}
  $('send').disabled=true;$('send').textContent='Enviando...';
  try{
    const photo=(await assets.upload($('pic').files[0])).id;
    await db.collection('rsvps').doc(me).set({family:fam,people:n,photo,at:Date.now()});
    aviso('¡Gracias, '+fam+'! Tu asistencia quedó confirmada. ¡Los espero con mucho cariño!','bien');petalos(40,true);
    $('send').textContent='¡Asistencia confirmada!';
  }catch(e){$('send').disabled=false;$('send').textContent='¡Confirmo mi asistencia!';porWhatsApp(fam)}''',
'''  if(!$('pic').files[0]){aviso('Falta el paso 3: sube la foto de tu familia, ¡es parte de la dinámica!','error');$('subir').classList.add('falta');$('subir').scrollIntoView({behavior:'smooth',block:'center'});return}
  if(!$('agree').checked){aviso('Marca que traerás un regalo de $1 por cada integrante.','error');$('comp').classList.add('falta');return}
  aviso('');
  /* Si la invitación está publicada en Claude, también se guarda en "Mis confirmaciones" */
  if(db&&me&&assets){
    $('send').disabled=true;$('send').textContent='Enviando...';
    try{
      const photo=(await assets.upload($('pic').files[0])).id;
      await db.collection('rsvps').doc(me).set({family:fam,people:n,photo,at:Date.now()});
    }catch(e){}
  }
  terminar(fam);''')

open(p, 'w', encoding='utf-8').write(s)
print('ok')
