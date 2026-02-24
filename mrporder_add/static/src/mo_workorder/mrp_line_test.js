// 按下BUTTON -> 前端fetch -> 後端controller -> model function -> 回傳JSON -> 觸發功能
(function () {
    const BUTTON_CLASS = 'mrporder-add-btn';
    const BUTTON_LABEL = 'Button';

    // 建button
    function createButton() {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-info ms-2 ' + BUTTON_CLASS;
        btn.textContent = BUTTON_LABEL;

        btn.addEventListener('click', async ev => {
            ev.stopPropagation();
            try {
                // 呼叫後端 JSON route
                const resp = await fetch("/mrp_show_info", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-Requested-With": "XMLHttpRequest"
                    },
                    credentials: "same-origin",
                    body: JSON.stringify({})
                });

                if (!resp.ok) {
                    alert('伺服器回應錯誤');
                    return;
                }

                const json = await resp.json(); // 解析 JSON
                const action = json.result || json; // 如是 JSON-RPC wrapper，取 result

                if (action && action.tag === 'display_notification' && action.params) {
                    alert((action.params.title ? action.params.title + '\n' : '') + action.params.message);
                } else {
                    // 其他情況顯示 JSON
                    alert('Received action: ' + JSON.stringify(action));
                }
            } catch (err) {
                alert('發生錯誤');
                console.error(err);
            }
        });
        return btn;
    }
    // 插入button到該footer
    function insertButton(footer) {
        if (!footer || footer.querySelector(`.${BUTTON_CLASS}`)) return;

        const targetBtn = Array.from(footer.querySelectorAll('button')).find(b =>
            /Close Production|Mark as Done|關閉生產/i.test(b.innerText) ||
            b.getAttribute('barcode_trigger') === 'cloMO' ||
            b.getAttribute('barcode_trigger') === 'cloWO'
        );
        // 在 targetBtn 後面，或 footer 最後
        if (targetBtn && targetBtn.parentNode) {
            targetBtn.insertAdjacentElement('afterend', createButton());
        } else {
            footer.appendChild(createButton());
        }
    }
    // 掃描現有 footer 並監控 DOM 動態新增 footer
    function scanAndObserve() {
        document.querySelectorAll('.card-footer').forEach(insertButton);
        const parent = document.querySelector('.o_mrp_display_records') || document.body;
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (!(node instanceof HTMLElement)) return;
                    const footer = node.matches('.card-footer') ? node : node.querySelector('.card-footer');
                    if (footer) insertButton(footer);
                });
            });
        });
        observer.observe(parent, { childList: true, subtree: true });
    }
    setTimeout(scanAndObserve, 50);
})();