# Pattern D — Modal Confirmation

> **Use for:** Confirmation dialogs (delete, archive, logout), simple 1-3 field forms.
> **NOT for:** Create/Edit forms (use Pattern B drawer slide-in).
> **Reference:** `core-marketing-prospect.html` — Confirm Modal pattern (lines 1411-1485).

---

## 🎯 When to Use

✅ Destructive confirmation (delete, archive, logout)
✅ Critical state-change confirmation (publish, finalize, approve)
✅ Simple 1-3 field input (invite by email, send message)
✅ Information acknowledgment (success/error notice)

❌ Multi-step process (use drawer)
❌ Create/Edit forms (use drawer — per user override)
❌ Detail view (use drawer)

---

## 🏗️ Structure

```
.modal-backdrop (click to close)
↓
.modal (440px max-width, centered, scale animation)
  ├─ .modal-header (icon + title + subtitle)
  ├─ .modal-body (message OR simple form fields)
  └─ .modal-footer (Cancel + Confirm buttons)
```

---

## 📋 HTML Skeleton — Destructive Confirmation (Delete)

```html
<div class="modal-backdrop ${state.modal.open ? 'is-open' : ''}" onclick="closeModal()">
  <div class="modal" onclick="event.stopPropagation()">

    <!-- HEADER -->
    <div class="modal-header">
      <div class="modal-header-icon is-danger">
        <i data-lucide="trash-2" class="w-5 h-5"></i>
      </div>
      <div style="flex: 1;">
        <h3 class="modal-title">ยืนยันการลบ Prospect</h3>
        <p class="modal-subtitle">
          คุณกำลังจะลบ <strong>${record.name}</strong> ออกจากระบบ การกระทำนี้ไม่สามารถยกเลิกได้
        </p>
      </div>
      <button class="icon-btn" onclick="closeModal()">
        <i data-lucide="x" class="w-4 h-4"></i>
      </button>
    </div>

    <!-- BODY (optional — additional context) -->
    <div class="modal-body">
      <div style="padding: 12px; background: #FFE9E7; border-radius: 8px; font-size: 12.5px; color: #991B1B;">
        <strong>คำเตือน:</strong> ข้อมูลที่ลบจะถูกย้ายไปยัง Trash และจะถูกลบถาวรหลัง 30 วัน
      </div>
    </div>

    <!-- FOOTER -->
    <div class="modal-footer">
      <button class="btn btn-ghost" onclick="closeModal()">ยกเลิก</button>
      <button class="btn btn-danger" onclick="confirmDelete('${record.id}')" 
              style="background: var(--c-danger); color: #fff; border-color: var(--c-danger);">
        <i data-lucide="trash-2" class="w-4 h-4"></i>
        <span>ลบทันที</span>
      </button>
    </div>

  </div>
</div>
```

---

## 📋 HTML Skeleton — Warning Confirmation (Archive)

```html
<div class="modal-backdrop is-open" onclick="closeModal()">
  <div class="modal" onclick="event.stopPropagation()">
    <div class="modal-header">
      <div class="modal-header-icon is-warning">
        <i data-lucide="archive" class="w-5 h-5"></i>
      </div>
      <div style="flex: 1;">
        <h3 class="modal-title">เก็บเข้า Archive</h3>
        <p class="modal-subtitle">
          ${record.name} จะถูกย้ายไปยัง Archived. ยังสามารถ Restore ได้ภายหลัง
        </p>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-ghost" onclick="closeModal()">ยกเลิก</button>
      <button class="btn btn-primary" onclick="confirmArchive('${record.id}')">
        <i data-lucide="archive" class="w-4 h-4"></i>
        <span>ยืนยันเก็บเข้า Archive</span>
      </button>
    </div>
  </div>
</div>
```

---

## 📋 HTML Skeleton — Simple Form (Invite by Email)

```html
<div class="modal-backdrop is-open" onclick="closeModal()">
  <div class="modal" onclick="event.stopPropagation()">
    <div class="modal-header">
      <div class="modal-header-icon">
        <i data-lucide="user-plus" class="w-5 h-5"></i>
      </div>
      <div style="flex: 1;">
        <h3 class="modal-title">เชิญสมาชิกใหม่</h3>
        <p class="modal-subtitle">ระบุอีเมลและ role ที่จะให้สมาชิกใหม่</p>
      </div>
      <button class="icon-btn" onclick="closeModal()">
        <i data-lucide="x" class="w-4 h-4"></i>
      </button>
    </div>

    <div class="modal-body">
      <div class="field">
        <label class="field-label">อีเมล <span class="req">*</span></label>
        <input class="input field-input" type="email" id="inv-email" placeholder="name@company.com">
      </div>
      <div class="field" style="margin-bottom: 0;">
        <label class="field-label">Role <span class="req">*</span></label>
        <select class="select field-input" id="inv-role">
          <option value="">เลือก role...</option>
          <option value="admin">Admin</option>
          <option value="editor">Editor</option>
          <option value="viewer">Viewer</option>
        </select>
      </div>
    </div>

    <div class="modal-footer">
      <button class="btn btn-ghost" onclick="closeModal()">ยกเลิก</button>
      <button class="btn btn-primary" onclick="submitInvite()">
        <i data-lucide="send" class="w-4 h-4"></i>
        <span>ส่งคำเชิญ</span>
      </button>
    </div>
  </div>
</div>
```

---

## 📋 HTML Skeleton — Info/Success Acknowledgment

```html
<div class="modal-backdrop is-open" onclick="closeModal()">
  <div class="modal" onclick="event.stopPropagation()">
    <div class="modal-header">
      <div class="modal-header-icon" style="background: #E4F4EB; color: var(--c-success);">
        <i data-lucide="check-circle-2" class="w-5 h-5"></i>
      </div>
      <div style="flex: 1;">
        <h3 class="modal-title">บันทึกสำเร็จ</h3>
        <p class="modal-subtitle">
          ข้อมูลของคุณถูกบันทึกเรียบร้อยแล้ว
        </p>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-primary" onclick="closeModal()" style="margin-left: auto;">
        เข้าใจแล้ว
      </button>
    </div>
  </div>
</div>
```

---

## 🔧 Required JS Helpers

```javascript
// State extension
// state.modal = { open, type: 'delete'|'archive'|'invite'|'info', data: {...} }

function openModal(type, data = {}) {
  state.modal = { open: true, type, data };
  render();
  requestAnimationFrame(() => {
    document.getElementById('modalBackdrop').classList.add('is-open');
  });
}

function closeModal() {
  document.getElementById('modalBackdrop').classList.remove('is-open');
  setTimeout(() => {
    state.modal = { open: false, type: null, data: null };
    render();
  }, 200);
}

// Confirmation handlers
function confirmDelete(id) {
  state.records = state.records.filter(r => r.id !== id);
  closeModal();
  closeDrawer();  // Also close drawer if open
  showToast('ลบสำเร็จ', 'success');
}

function confirmArchive(id) {
  const r = state.records.find(x => x.id === id);
  if (r) r.status = 'archived';
  closeModal();
  showToast('เก็บเข้า Archive แล้ว', 'success');
}

function submitInvite() {
  const email = document.getElementById('inv-email').value.trim();
  const role = document.getElementById('inv-role').value;
  if (!email || !role) {
    showToast('กรุณากรอกข้อมูลให้ครบ', 'warning');
    return;
  }
  closeModal();
  showToast(`ส่งคำเชิญถึง ${email} แล้ว`, 'success');
}
```

---

## 🎨 Modal Variants Summary

| Variant | Icon | Icon BG color | Primary Button |
|---|---|---|---|
| **Default (info)** | `info` / `user-plus` / etc | `rgba(255,59,48,0.10)` + `--c-primary` | `.btn-primary` |
| **Danger (destructive)** | `trash-2` / `x-octagon` | `#FFE9E7` + `--c-danger` | `.btn-danger` solid red |
| **Warning (caution)** | `alert-triangle` / `archive` | `#FFF1DD` + `--c-warning` | `.btn-primary` |
| **Success (acknowledge)** | `check-circle-2` | `#E4F4EB` + `--c-success` | `.btn-primary` |

---

## 🛡️ Iron Rules to Enforce

- **#11** Modal width 440px (max-width 92vw) ✓
- **#14** Modal for confirmation only — NOT for create/edit (use drawer) ✓
- **#15** 3 close methods: backdrop / X / Esc ✓
- **#18** If form: field/field-label/field-input structure ✓
- **#21** All `<i data-lucide>` have `w-{N} h-{N}` ✓
- **#23** No color emoji ✓

---

## ⚠️ Common Mistakes

1. **❌** Using modal for multi-step form (use drawer)
2. **❌** Using modal for full record create (use drawer slide-in)
3. **❌** Modal wider than 440px without max-width (responsive breaks on mobile)
4. **❌** No `event.stopPropagation()` on modal click → closes when clicking inside
5. **❌** Danger action with `.btn-primary` style (must use danger variant — red bg)
6. **❌** No icon in modal header (always include semantic icon)
7. **❌** Cancel button on right, Confirm on left (always Cancel left, Primary right)
8. **❌** Submit button enabled when form invalid (validate before submit)

---

## 🎯 Confirmation Pattern Best Practice

For **destructive actions** (delete, hard archive):
- Show the **record name** in subtitle ("คุณกำลังจะลบ **John Smith**")
- Use **red danger button** with verb ("ลบทันที", not just "ยืนยัน")
- Optional: extra warning box in body for highly destructive actions

For **soft actions** (archive, suspend):
- Use warning style (yellow/orange icon)
- Mention reversibility ("ยังสามารถ Restore ได้ภายหลัง")
- Use primary button (not danger)
