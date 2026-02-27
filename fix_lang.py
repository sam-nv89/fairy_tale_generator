import re

with open('landing.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace the dropdown options html generation logic
old_dropdown_gen = """    # Build HTML <option> list with the current language pre-selected
    options_html = ""
    for code, name in sorted(lang_options.items(), key=lambda x: x[1]):
        selected = 'selected' if code == current_lang else ''
        options_html += f'<option value="{code}" {selected}>{name}</option>\\n'"""

new_dropdown_gen = """    # Build HTML for language options dropdown
    current_lang_name = lang_options.get(current_lang, current_lang.upper())
    options_html = f'''
    <div class="lang-dropdown">
        <button class="lang-dropbtn">🌍 {current_lang_name} ▾</button>
        <div class="lang-dropdown-content">
    '''
    for code, name in sorted(lang_options.items(), key=lambda x: x[1]):
        active_style = 'font-weight: bold; color: #a78bfa;' if code == current_lang else ''
        options_html += f'<a href="?lang={code}" style="{active_style}">{name}</a>\\n'
    options_html += '''
        </div>
    </div>
    '''"""

text = text.replace(old_dropdown_gen, new_dropdown_gen)

# 2. Replace the CSS for .lang-select-nav with .lang-dropdown
old_css = """/* Language selector */
.lang-select-nav {
    appearance: none;
    -webkit-appearance: none;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 8px;
    color: white;
    font-size: 0.85rem;
    font-family: inherit;
    font-weight: 500;
    padding: 0.4rem 2rem 0.4rem 0.8rem;
    cursor: pointer;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 0.6rem center;
    outline: none;
    transition: background-color 0.2s ease, border-color 0.2s ease;
}
.lang-select-nav:hover {
    background: rgba(255,255,255,0.1);
    border-color: rgba(255,255,255,0.3);
}
.lang-select-nav option {
    background: #1e293b;
    color: white;
}"""

new_css = """/* Language Dropdown */
.lang-dropdown {
    position: relative;
    display: inline-block;
}

.lang-dropbtn {
    background: rgba(255, 255, 255, 0.05);
    color: white;
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s;
    outline: none;
}

.lang-dropdown:hover .lang-dropbtn {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255,255,255,0.3);
}

.lang-dropdown-content {
    display: none;
    position: absolute;
    right: 0;
    top: 100%;
    margin-top: 0.5rem;
    background: rgba(15, 23, 42, 0.95);
    min-width: 140px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    z-index: 1000;
    overflow: hidden;
    backdrop-filter: blur(10px);
}

.lang-dropdown:hover .lang-dropdown-content {
    display: block;
    animation: fadeIn 0.15s ease;
}

.lang-dropdown-content a {
    color: white;
    padding: 0.8rem 1rem;
    text-decoration: none;
    display: block;
    font-size: 0.95rem;
    transition: background 0.2s;
}

.lang-dropdown-content a:hover {
    background: rgba(255, 255, 255, 0.1);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-5px); }
    to { opacity: 1; transform: translateY(0); }
}"""

text = text.replace(old_css, new_css)

# 3. Mobile CSS
old_mobile_css = """.mobile-menu-overlay .lang-select-nav {
        font-size: 1.2rem;
        padding: 0.8rem 3rem 0.8rem 1.5rem;
        border-radius: 12px;
        background-position: right 1rem center;
    }"""

new_mobile_css = """.mobile-menu-overlay .lang-dropdown {
        font-size: 1.2rem;
        margin-top: 1rem;
    }
    .mobile-menu-overlay .lang-dropbtn {
        font-size: 1.1rem;
        padding: 0.8rem 1.5rem;
    }
    .mobile-menu-overlay .lang-dropdown-content {
        position: static;
        display: block;
        box-shadow: none;
        background: transparent;
        border: none;
        margin-top: 0;
    }
    .mobile-menu-overlay .lang-dropdown-content a {
        padding: 0.5rem 1.5rem;
        font-size: 1rem;
        color: #94a3b8;
    }
    .mobile-menu-overlay .lang-dropdown-content a:hover {
        color: white;
        background: transparent;
    }"""

text = text.replace(old_mobile_css, new_mobile_css)


# 4. Replace <select class="lang-select-nav" id="..."> \n {options_html} \n </select> with {options_html}
text = re.sub(r'<select class="lang-select-nav".*?>(.*?)</select>', r'\1', text, flags=re.DOTALL)


# 5. Remove the tricky iframe JS handleLangChange completely
old_js = """    var doc = window.parent.document;
    function attachListener() {
        var dpPicker = doc.getElementById('langPickerNav_desktop');
        var mbPicker = doc.getElementById('langPickerNav_mobile');
        var attachedCount = 0;
        
        function handleLangChange(e) {
            var langCode = e.target.value;
            var url = new URL(window.parent.location.href);
            url.searchParams.set('lang', langCode);
            window.parent.location.href = url.toString();
        }
        
        if (dpPicker && !dpPicker.dataset.listenerAttached) {
            dpPicker.dataset.listenerAttached = "true";
            dpPicker.addEventListener('change', handleLangChange);
            attachedCount++;
        }
        if (mbPicker && !mbPicker.dataset.listenerAttached) {
            mbPicker.dataset.listenerAttached = "true";
            mbPicker.addEventListener('change', handleLangChange);
            attachedCount++;
        }
        
        // Auto-close hamburger when a link is clicked
        var mobileLinks = doc.querySelectorAll('.mobile-link');
        var toggle = doc.getElementById('mobile-menu-toggle');
        if (mobileLinks.length > 0 && toggle && !toggle.dataset.listenerAttached) {
            toggle.dataset.listenerAttached = "true";
            Array.from(mobileLinks).forEach(function(link) {
                link.addEventListener('click', function() {
                    toggle.checked = false;
                });
            });
            attachedCount++;
        }
        
        return (dpPicker != null || mbPicker != null);
    }
    
    // Attempt multiple times because DOM render might be slightly delayed
    var pollId = setInterval(function() {
        if (attachListener()) {
            clearInterval(pollId);
        }
    }, 100);
    setTimeout(function() { clearInterval(pollId); }, 5000);"""

new_js = """    var doc = window.parent.document;
    function attachListener() {
        var attachedCount = 0;
        
        // Auto-close hamburger when a link is clicked
        var mobileLinks = doc.querySelectorAll('.mobile-link');
        var toggle = doc.getElementById('mobile-menu-toggle');
        if (mobileLinks.length > 0 && toggle && !toggle.dataset.listenerAttached) {
            toggle.dataset.listenerAttached = "true";
            Array.from(mobileLinks).forEach(function(link) {
                link.addEventListener('click', function() {
                    toggle.checked = false;
                });
            });
            attachedCount++;
            return true;
        }
        return false;
    }
    
    var pollId = setInterval(function() {
        if (attachListener()) {
            clearInterval(pollId);
        }
    }, 200);
    setTimeout(function() { clearInterval(pollId); }, 3000);"""

text = text.replace(old_js, new_js)

with open('landing.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Replacement logic done.")
