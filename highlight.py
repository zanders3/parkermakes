"""Small, dependency-free syntax highlighter for C-family code fences."""

from html import escape, unescape
import re


LANGUAGES = {
    'c': 'c',
    'h': 'c',
    'cc': 'cpp',
    'cpp': 'cpp',
    'c++': 'cpp',
    'cxx': 'cpp',
    'hpp': 'cpp',
    'cs': 'csharp',
    'csharp': 'csharp',
    'sh': 'shell',
    'shell': 'shell',
    'bash': 'shell',
    'zsh': 'shell',
    'ld': 'ld',
    'ldscript': 'ld',
    'linker-script': 'ld',
    'asm': 'nasm',
    'nasm': 'nasm',
}

COMMON_KEYWORDS = {
    'break', 'case', 'continue', 'default', 'do', 'else', 'for', 'goto', 'if',
    'return', 'sizeof', 'switch', 'while',
}
C_KEYWORDS = COMMON_KEYWORDS | {
    '_Alignas', '_Alignof', '_Atomic', '_Generic', '_Noreturn', '_Static_assert',
    '_Thread_local', 'auto', 'const', 'enum', 'extern', 'inline', 'register',
    'restrict', 'static', 'struct', 'typedef', 'union', 'volatile',
}
CPP_KEYWORDS = C_KEYWORDS | {
    'alignas', 'alignof', 'and', 'and_eq', 'asm', 'bitand', 'bitor', 'catch',
    'class', 'compl', 'concept', 'consteval', 'constexpr', 'constinit',
    'const_cast', 'co_await', 'co_return', 'co_yield', 'decltype', 'delete',
    'dynamic_cast', 'explicit', 'export', 'friend', 'mutable', 'namespace', 'new',
    'noexcept', 'not', 'not_eq', 'operator', 'or', 'or_eq', 'private',
    'protected', 'public', 'reinterpret_cast', 'requires', 'static_assert',
    'static_cast', 'template', 'this', 'thread_local', 'throw', 'try', 'typeid',
    'typename', 'using', 'virtual', 'xor', 'xor_eq',
}
CSHARP_KEYWORDS = COMMON_KEYWORDS | {
    'abstract', 'as', 'async', 'await', 'base', 'checked', 'class', 'const',
    'delegate', 'event', 'explicit', 'extern', 'finally', 'fixed', 'foreach',
    'get', 'implicit', 'in', 'interface', 'internal', 'is', 'lock', 'namespace',
    'new', 'operator', 'out', 'override', 'params', 'partial', 'private',
    'protected', 'public', 'readonly', 'record', 'ref', 'required', 'sealed',
    'set', 'stackalloc', 'static', 'struct', 'this', 'throw', 'try', 'typeof',
    'unchecked', 'unsafe', 'using', 'value', 'virtual', 'volatile', 'when',
    'where', 'yield',
}
TYPES = {
    'bool', 'byte', 'char', 'decimal', 'double', 'dynamic', 'float', 'int',
    'int8_t', 'int16_t', 'int32_t', 'int64_t', 'long', 'nint', 'nuint', 'object',
    'sbyte', 'short', 'signed', 'size_t', 'string', 'uint', 'uint8_t',
    'uint16_t', 'uint32_t', 'uint64_t', 'ulong', 'unsigned', 'ushort', 'var',
    'void', 'wchar_t',
}
LITERALS = {'false', 'null', 'nullptr', 'true'}
KEYWORDS = {'c': C_KEYWORDS, 'cpp': CPP_KEYWORDS, 'csharp': CSHARP_KEYWORDS}
SHELL_KEYWORDS = {
    'case', 'do', 'done', 'elif', 'else', 'esac', 'fi', 'for', 'function', 'if',
    'in', 'select', 'then', 'time', 'until', 'while',
}
SHELL_BUILTINS = {
    'alias', 'break', 'cd', 'command', 'continue', 'declare', 'echo', 'eval',
    'exec', 'exit', 'export', 'local', 'printf', 'pwd', 'read', 'readonly',
    'return', 'set', 'shift', 'source', 'test', 'trap', 'type', 'typeset',
    'unalias', 'unset',
}
SHELL_COMMANDS = {
    'apt-get', 'brew', 'cmake', 'gcc', 'git', 'i386-elf-_g++', 'make', 'nasm',
    'python', 'python3', 'qemu-system-x86_64', 'sudo', 'xcode-select',
}
LD_KEYWORDS = {
    'ABSOLUTE', 'ADDR', 'ALIGN', 'ALIGNOF', 'ASSERT', 'AT', 'BLOCK', 'BYTE',
    'CONSTANT', 'COPY', 'CREATE_OBJECT_SYMBOLS', 'DEFINED', 'DSECT', 'ENTRY',
    'EXCLUDE_FILE', 'EXTERN', 'FILL', 'FORCE_COMMON_ALLOCATION', 'GROUP',
    'INCLUDE', 'INHIBIT_COMMON_ALLOCATION', 'INPUT', 'KEEP', 'LENGTH', 'LOADADDR',
    'LONG', 'MAX', 'MEMORY', 'MIN', 'NEXT', 'NOLOAD', 'ORIGIN', 'OUTPUT',
    'OUTPUT_ARCH', 'OUTPUT_FORMAT', 'OVERLAY', 'PHDRS', 'PROVIDE',
    'PROVIDE_HIDDEN', 'QUAD', 'SEARCH_DIR', 'SECTIONS', 'SHORT', 'SIZEOF',
    'SIZEOF_HEADERS', 'SORT', 'SORT_BY_ALIGNMENT', 'SORT_BY_INIT_PRIORITY',
    'SORT_BY_NAME', 'SQUAD', 'STARTUP', 'SUBALIGN', 'TARGET', 'VERSION',
}
NASM_DIRECTIVES = {
    'align', 'bits', 'common', 'db', 'dd', 'do', 'dq', 'dt', 'dw', 'dy', 'dz',
    'endstruc', 'equ', 'extern', 'global', 'istruc', 'org', 'resb', 'resd',
    'reso', 'resq', 'rest', 'resw', 'resy', 'resz', 'section', 'segment',
    'struc', 'times', 'use16', 'use32', 'use64', 'wrt',
}
NASM_INSTRUCTIONS = {
    'adc', 'add', 'and', 'call', 'cli', 'cmp', 'dec', 'div', 'hlt', 'idiv',
    'imul', 'in', 'inc', 'int', 'iret', 'ja', 'jae', 'jb', 'jbe', 'je', 'jg',
    'jge', 'jl', 'jle', 'jmp', 'jne', 'jno', 'jnp', 'jns', 'jo', 'jp', 'js',
    'jz', 'lea', 'lgdt', 'lidt', 'lodsb', 'loop', 'mov', 'movsb', 'mul', 'neg',
    'nop', 'not', 'or', 'out', 'pop', 'push', 'ret', 'rol', 'ror', 'sal', 'sar',
    'sbb', 'shl', 'shr', 'sti', 'stosb', 'sub', 'test', 'xor',
}
NASM_REGISTERS = {
    'al', 'ah', 'ax', 'eax', 'rax', 'bl', 'bh', 'bx', 'ebx', 'rbx', 'cl', 'ch',
    'cx', 'ecx', 'rcx', 'dl', 'dh', 'dx', 'edx', 'rdx', 'si', 'esi', 'rsi',
    'di', 'edi', 'rdi', 'sp', 'esp', 'rsp', 'bp', 'ebp', 'rbp', 'cs', 'ds',
    'es', 'fs', 'gs', 'ss', 'cr0', 'cr2', 'cr3', 'cr4', 'word', 'dword',
    'qword', 'byte',
}

CODE_BLOCK_RE = re.compile(
    r'(?P<open><pre(?:\s[^>]*)?><code(?P<attrs>[^>]*)>)'
    r'(?P<code>.*?)'
    r'(?P<close></code></pre>)',
    re.DOTALL,
)
CLASS_RE = re.compile(r'''\bclass\s*=\s*(["'])(?P<classes>.*?)\1''', re.DOTALL)
IDENTIFIER_RE = re.compile(r'[A-Za-z_]\w*')
NUMBER_RE = re.compile(
    r'(?:0[xX][0-9A-Fa-f](?:_?[0-9A-Fa-f])*'
    r'|0[bB][01](?:_?[01])*'
    r'|(?:\d(?:_?\d)*)(?:\.\d(?:_?\d)*)?(?:[eE][+-]?\d(?:_?\d)*)?)'
    r'(?:[uUlLfFdDmM]|ul|UL|ll|LL)*'
)
NASM_NUMBER_RE = re.compile(
    r'(?:0[xX][0-9A-Fa-f](?:_?[0-9A-Fa-f])*'
    r'|0[bB][01](?:_?[01])*'
    r'|[0-9](?:_?[0-9A-Fa-f])*[hH]'
    r'|[01](?:_?[01])*[bB]'
    r'|\d(?:_?\d)*)'
)
SHELL_VARIABLE_RE = re.compile(
    r'\$(?:\{[^}\n]+\}|[A-Za-z_][A-Za-z0-9_]*|[0-9@*#?$!_-])'
)
SHELL_WORD_RE = re.compile(r'[A-Za-z_][A-Za-z0-9_+.-]*')


def _span(kind, text):
    return f'<span class="token-{kind}">{escape(text, quote=False)}</span>'


def _quoted_end(source, start, quote, verbatim=False):
    """Return the first position after a quoted string, or the end of input."""
    i = start + 1
    while i < len(source):
        if source[i] == quote:
            if verbatim and i + 1 < len(source) and source[i + 1] == quote:
                i += 2
                continue
            return i + 1
        if not verbatim and source[i] == '\\' and i + 1 < len(source):
            i += 2
        else:
            i += 1
    return len(source)


def highlight(source, language):
    """Return escaped source with basic C-family token spans."""
    family = LANGUAGES.get(language.lower())
    if not family:
        return None

    output = []
    i = 0
    while i < len(source):
        if family == 'nasm' and source[i] == ';':
            end = source.find('\n', i)
            end = len(source) if end < 0 else end
            output.append(_span('comment', source[i:end]))
            i = end
            continue
        if family == 'shell' and source[i] == '#':
            end = source.find('\n', i)
            end = len(source) if end < 0 else end
            output.append(_span('comment', source[i:end]))
            i = end
            continue
        if family in ('c', 'cpp', 'csharp', 'ld') and source.startswith('//', i):
            end = source.find('\n', i)
            end = len(source) if end < 0 else end
            output.append(_span('comment', source[i:end]))
            i = end
            continue
        if family in ('c', 'cpp', 'csharp', 'ld') and source.startswith('/*', i):
            end = source.find('*/', i + 2)
            end = len(source) if end < 0 else end + 2
            output.append(_span('comment', source[i:end]))
            i = end
            continue

        line_start = source.rfind('\n', 0, i) + 1
        if family in ('c', 'cpp', 'csharp') and source[i] == '#' and not source[line_start:i].strip():
            end = source.find('\n', i)
            end = len(source) if end < 0 else end
            output.append(_span('preprocessor', source[i:end]))
            i = end
            continue
        if family == 'nasm' and source[i] == '%':
            end = source.find('\n', i)
            end = len(source) if end < 0 else end
            output.append(_span('directive', source[i:end]))
            i = end
            continue

        if family == 'shell' and source[i] == '$':
            variable = SHELL_VARIABLE_RE.match(source, i)
            if variable:
                output.append(_span('variable', variable.group()))
                i = variable.end()
                continue

        # C# permits @"verbatim", $"interpolated", and combined $@/@$ strings.
        string_prefix = ''
        if family == 'csharp':
            string_prefix = next((prefix for prefix in ('$@', '@$', '@', '$')
                                  if source.startswith(prefix + '"', i)), '')
        elif family in ('c', 'cpp'):
            string_prefix = next((prefix for prefix in ('u8', 'u', 'U', 'L')
                                  if source.startswith(prefix + '"', i)), '')
        if string_prefix or source[i] in ('"', "'"):
            quote_at = i + len(string_prefix)
            quote = source[quote_at]
            end = _quoted_end(source, quote_at, quote,
                              verbatim=family == 'csharp' and '@' in string_prefix)
            output.append(_span('string', source[i:end]))
            i = end
            continue

        number = (NASM_NUMBER_RE if family == 'nasm' else NUMBER_RE).match(source, i)
        if number:
            output.append(_span('number', number.group()))
            i = number.end()
            continue

        identifier = (SHELL_WORD_RE if family == 'shell' else IDENTIFIER_RE).match(source, i)
        if identifier:
            word = identifier.group()
            lower = word.lower()
            if family in KEYWORDS and word in KEYWORDS[family]:
                output.append(_span('keyword', word))
            elif family in ('c', 'cpp', 'csharp') and word in TYPES:
                output.append(_span('type', word))
            elif family in ('c', 'cpp', 'csharp') and word in LITERALS:
                output.append(_span('literal', word))
            elif family == 'shell' and word in SHELL_KEYWORDS:
                output.append(_span('keyword', word))
            elif family == 'shell' and word in SHELL_BUILTINS:
                output.append(_span('builtin', word))
            elif family == 'shell' and word in SHELL_COMMANDS:
                output.append(_span('command', word))
            elif family == 'ld' and word.upper() in LD_KEYWORDS:
                output.append(_span('keyword', word))
            elif family == 'nasm' and lower in NASM_DIRECTIVES:
                output.append(_span('directive', word))
            elif family == 'nasm' and lower in NASM_INSTRUCTIONS:
                output.append(_span('keyword', word))
            elif family == 'nasm' and lower in NASM_REGISTERS:
                output.append(_span('register', word))
            else:
                output.append(escape(word, quote=False))
            i = identifier.end()
            continue

        output.append(escape(source[i], quote=False))
        i += 1
    return ''.join(output)


def highlight_code_blocks(html):
    """Highlight supported fenced blocks in Markdown-generated HTML."""
    def replace(match):
        class_match = CLASS_RE.search(match['attrs'])
        if not class_match:
            return match.group()
        language = next((name.removeprefix('language-')
                         for name in class_match['classes'].split()
                         if name.startswith('language-')), '')
        highlighted = highlight(unescape(match['code']), language)
        if highlighted is None:
            return match.group()
        return match['open'] + highlighted + match['close']

    return CODE_BLOCK_RE.sub(replace, html)
