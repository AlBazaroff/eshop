// Content modal / dynamic add/delete JS
(() => {
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
        }
    }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
const btnAddContent = document.getElementById('btnAddContent');
const addUrl = btnAddContent ? btnAddContent.dataset.addUrl : null;
const deleteBase = btnAddContent ? btnAddContent.dataset.deleteBase : null; // includes '0' placeholder
const contentModalEl = document.getElementById('contentModal');
// const contentModal = new bootstrap.modal('#contentModal');
const contentForm = document.getElementById('contentForm');
const contentTypeSelect = document.getElementById('contentTypeSelect');
const fieldImage = document.getElementById('fieldImage');
const fieldVideo = document.getElementById('fieldVideo');
const imageItems = document.getElementById('imageItems');
const videoItems = document.getElementById('videoItems');

let bsModal = null;
try { if (contentModalEl) bsModal = new bootstrap.Modal(contentModalEl); } catch (e) { /* bootstrap not available */ }

// Reset modal inputs and selection when modal is closed (so it doesn't remember previous values)
if (contentModalEl) {
    contentModalEl.addEventListener('hidden.bs.modal', () => {
        try {
            if (contentForm) contentForm.reset();
            showFieldFor('');
            if (contentTypeSelect) contentTypeSelect.value = '';
            const fileInput = document.getElementById('id_content_file');
            if (fileInput) fileInput.value = '';
            const urlInput = document.getElementById('id_content_url');
            if (urlInput) urlInput.value = '';
        } catch (e) {
            // ignore
        }
    });
}

function showFieldFor(type) {
    if (!fieldImage || !fieldVideo) return;
    if (type === 'image') {
    fieldImage.classList.remove('d-none');
    fieldVideo.classList.add('d-none');
    } else if (type === 'video') {
    fieldImage.classList.add('d-none');
    fieldVideo.classList.remove('d-none');
    } else {
    fieldImage.classList.add('d-none');
    fieldVideo.classList.add('d-none');
    }
}

// Prefer delegated change handling on the modal so the listener works even
// if the modal content is re-rendered or the select is re-created.
if (contentModalEl) {
    contentModalEl.addEventListener('change', (e) => {
        if (e.target && e.target.id === 'contentTypeSelect') {
            showFieldFor(e.target.value);
        }
    });
}

if (contentForm) {
    contentForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!addUrl) { alert('Upload URL not available'); return; }
    // read select value at submit time (in case the element was re-created)
    const sel = document.getElementById('contentTypeSelect');
    const type = sel ? sel.value : '';
    if (!type) { alert('Choose content type'); return; }

    const fd = new FormData();
    fd.append('type', type);
    if (type === 'image') {
        const fileInput = document.getElementById('id_content_file');
        if (!fileInput || !fileInput.files || !fileInput.files.length) { alert('Choose image file'); return; }
        fd.append('content', fileInput.files[0]);
    } else {
        const urlInput = document.getElementById('id_content_url');
        if (!urlInput || !urlInput.value) { alert('Enter video URL'); return; }
        fd.append('content', urlInput.value);
    }

    try {
        const resp = await fetch(addUrl, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        body: fd,
        });
        const data = await resp.json();
        if (!resp.ok || !data.success) {
        const err = data.error || data.errors || JSON.stringify(data);
        alert(err);
        return;
        }

        const newItem = data.new_item;
        const contentId = data.content_id;
        if (type === 'image') {
        const div = document.createElement('div');
        div.className = 'position-relative content-item';
        div.dataset.contentId = contentId;
        const img = document.createElement('img');
        img.className = 'img-thumbnail';
        img.src = newItem.content;
        div.appendChild(img);
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-sm btn-outline-danger position-absolute top-0 end-0 btn-delete-content';
        btn.dataset.contentId = contentId;
        btn.innerHTML = '<i class="bi bi-x-lg"></i>';
        div.appendChild(btn);
            if (imageItems) {
            // remove empty message if present
            const empty = imageItems.querySelector('p');
            if (empty && /No additional images yet/.test(empty.textContent)) empty.remove();
            imageItems.appendChild(div);
            }
        } else {
        const wrap = document.createElement('div');
        wrap.className = 'content-item mb-3';
        wrap.dataset.contentId = contentId;
        const ratio = document.createElement('div');
        ratio.className = 'ratio ratio-16x9';
        const iframe = document.createElement('iframe');
        iframe.src = newItem.content;
        iframe.title = "YouTube video player"
        iframe.setAttribute('frameborder', '0');
        iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
        iframe.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
        iframe.setAttribute('allowfullscreen', '');
        ratio.appendChild(iframe);
        wrap.appendChild(ratio);
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-sm btn-outline-danger mt-2 btn-delete-content';
        btn.dataset.contentId = contentId;
        btn.textContent = 'Delete';
        wrap.appendChild(btn);
            if (videoItems) {
            const empty = videoItems.querySelector('p');
            if (empty && /No videos yet/.test(empty.textContent)) empty.remove();
            videoItems.appendChild(wrap);
            }
        }

        // reset and hide modal
        contentForm.reset();
        showFieldFor('');
        if (bsModal) bsModal.hide();
    } catch (err) {
        console.error(err);
        alert('Upload failed');
    }
    });
}

// delegated delete handler
document.addEventListener('click', async (e) => {
    const del = e.target.closest('.btn-delete-content');
    if (!del) return;
    const pcid = del.dataset.contentId;
    if (!pcid) return;
    if (!confirm('Are you sure you want to delete this item?')) return;
    if (!deleteBase) { alert('Delete URL not available'); return; }
    const url = deleteBase.replace('/0/', '/' + pcid + '/');
    try {
    const resp = await fetch(url, { method: 'POST', headers: { 'X-CSRFToken': csrftoken } });
    const data = await resp.json();
    if (resp.ok && data.success) {
        const el = document.querySelector(`[data-content-id="${pcid}"]`);
        if (el) el.remove();
        // if container now empty - add empty message back
        // determine whether it was image or video by searching containers
        const imgContainer = document.getElementById('imageItems');
        const vidContainer = document.getElementById('videoItems');
        if (imgContainer && imgContainer.querySelectorAll('.content-item').length === 0) {
            if (!imgContainer.querySelector('p')) {
                const p = document.createElement('p');
                p.textContent = 'No additional images yet';
                imgContainer.appendChild(p);
            }
        }
        if (vidContainer && vidContainer.querySelectorAll('.content-item').length === 0) {
            if (!vidContainer.querySelector('p')) {
                const p = document.createElement('p');
                p.textContent = 'No videos yet';
                vidContainer.appendChild(p);
            }
        }
    } else {
        alert(data.error || 'Delete failed');
    }
    } catch (err) {
    console.error(err);
    alert('Delete failed');
    }
});
})();