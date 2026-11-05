'use strict';
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.textContent = open ? 'Close' : 'Menu';
  navigation.classList.toggle('is-open', open);
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') {
    menuButton.click(); menuButton.focus();
  }
});
const filters = [...document.querySelectorAll('.filter')];
const figures = [...document.querySelectorAll('.gallery figure')];
filters.forEach(button => button.addEventListener('click', () => {
  filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  figures.forEach(figure => { figure.hidden = button.dataset.filter !== 'all' && figure.dataset.category !== button.dataset.filter; });
  const count = figures.filter(figure => !figure.hidden).length;
  document.querySelector('.gallery-count').textContent = `${count} photographs · ${button.textContent}`;
}));
const lightbox = document.querySelector('.lightbox');
let activePhoto = 0;
let previousFocus;
const photos = () => [...document.querySelectorAll('.gallery figure:not([hidden]) button')];
function showPhoto(index) {
  const list = photos();
  activePhoto = (index + list.length) % list.length;
  const selected = list[activePhoto];
  const image = lightbox.querySelector('img');
  image.src = selected.dataset.full;
  image.alt = selected.querySelector('img').alt;
  lightbox.querySelector('.lightbox-caption').textContent = image.alt;
  lightbox.querySelector('.lightbox-counter').textContent = `${activePhoto + 1} / ${list.length}`;
}
figures.forEach(figure => figure.querySelector('button')?.addEventListener('click', event => {
  previousFocus = event.currentTarget;
  showPhoto(photos().indexOf(previousFocus));
  lightbox.showModal();
}));
lightbox?.querySelector('[data-close]').addEventListener('click', () => lightbox.close());
lightbox?.querySelector('[data-prev]').addEventListener('click', () => showPhoto(activePhoto - 1));
lightbox?.querySelector('[data-next]').addEventListener('click', () => showPhoto(activePhoto + 1));
lightbox?.addEventListener('close', () => previousFocus?.focus());
lightbox?.addEventListener('keydown', event => {
  if(event.key === 'ArrowRight'){event.preventDefault();showPhoto(activePhoto + 1);}
  if(event.key === 'ArrowLeft'){event.preventDefault();showPhoto(activePhoto - 1);}
});
lightbox?.addEventListener('click', event => { if (event.target === lightbox) {
  const r=lightbox.getBoundingClientRect();
  if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)lightbox.close();
}});
const form=document.querySelector('#inquiry-form');
if(form){
  const requested=new URLSearchParams(location.search).get('session');
  const session=form.elements.session;
  if([...session.options].some(option=>option.value===requested))session.value=requested;
  form.addEventListener('submit', async event=>{
    event.preventDefault();
    if(!form.reportValidity())return;
    const fields=new FormData(form);
    const date=fields.get('date')||'Flexible';
    const draft=`Hi Trevor,\n\nI'd love to talk about a ${fields.get('session')} session.\n\nName: ${fields.get('name')}\nEmail: ${fields.get('email')}\nPhone: ${fields.get('phone')||'Not provided'}\nPreferred date: ${date}\nLocation: ${fields.get('location')||'Open to ideas'}\n\n${fields.get('message')}\n\nThank you!`;
    const output=document.querySelector('#inquiry-output');
    output.hidden=false;
    output.querySelector('textarea').value=draft;
    const email=form.dataset.email;
    output.querySelector('[data-email-draft]').href=`mailto:${email}?subject=${encodeURIComponent('Photography inquiry — '+fields.get('session'))}&body=${encodeURIComponent(draft)}`;
    document.querySelector('#form-status').textContent='Your inquiry is ready. Open it in your email app and send it to Trevor, or copy it below. Nothing has been sent yet.';
    output.querySelector('h2').focus();
  });
  document.querySelector('[data-copy]').addEventListener('click',async()=>{
    const draft=document.querySelector('#draft-text');
    try{await navigator.clipboard.writeText(draft.value);document.querySelector('#copy-status').textContent='Copied. Paste it into an email to trevoradair2@gmail.com.';}
    catch{draft.focus();draft.select();document.querySelector('#copy-status').textContent='Select and copy the message, then paste it into your email app.';}
  });
}
