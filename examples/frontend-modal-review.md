# The modal that only worked with a mouse

Playbook: [`frontend`](../playbooks/frontend/CLAUDE.md) — alias `ap-fe`

A modal component that looks fine in the browser and demos well. The playbook reviews it in its mandated shape and finds it unusable by keyboard, invisible to screen readers, and carrying state that can drift.

## Session (abridged)

**You:**

````text
Review this component:

```tsx
export function Modal({ isOpen, onClose, title, children }) {
  const [visible, setVisible] = useState(isOpen);

  useEffect(() => {
    setVisible(isOpen);
  }, [isOpen]);

  if (!visible) return null;
  return (
    <div className="overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-close" onClick={onClose}>×</div>
        <h2>{title}</h2>
        {children}
      </div>
    </div>
  );
}
```
````

**ap-fe:**

> ```text
> Critical issues:
>   1. Close control is a div with onClick — no keyboard access, no focus, no
>      accessible name, invisible to assistive tech. This alone fails the
>      component.
>   2. No Escape handling, no focus trap, no focus restore. Keyboard users can
>      tab behind the overlay into the page and cannot dismiss the dialog.
>   3. `visible` mirrors `isOpen` via state + effect — derived state that can
>      drift and re-renders twice on every toggle. It adds nothing.
>
> Accessibility:
>   - No dialog semantics: needs `role="dialog"`, `aria-modal="true"`, and
>     `aria-labelledby` pointing at the title — or better, the native
>     `<dialog>` element, which gives you focus containment, Escape, and
>     top-layer rendering for free.
>   - Overlay click-to-close with no visible close *button* leaves
>     screen-reader users with no discoverable exit.
>
> State/data flow:
>   - Delete `visible`; render on `isOpen` directly. The parent owns this
>     state — the component should not keep a shadow copy.
>
> Performance:
>   - Fine at this size. The effect-mirror is the only waste; removing it
>     removes the double render.
>
> Maintainability:
>   - Untyped props; `onClose` fires for overlay and button through different
>     paths — one `close()` seam makes the behavior testable.
>
> Suggested patch (core):
>   export function Modal({ isOpen, onClose, title, children }: ModalProps) {
>     const ref = useRef<HTMLDialogElement>(null);
>     useEffect(() => {
>       const d = ref.current;
>       if (!d) return;
>       if (isOpen && !d.open) d.showModal();   // traps focus, handles Esc
>       if (!isOpen && d.open) d.close();
>     }, [isOpen]);
>     return (
>       <dialog ref={ref} aria-labelledby="modal-title" onClose={onClose}
>               onClick={(e) => e.target === ref.current && onClose()}>
>         <button type="button" onClick={onClose} aria-label="Close">×</button>
>         <h2 id="modal-title">{title}</h2>
>         {children}
>       </dialog>
>     );
>   }
>
> Verification:
>   - Keyboard only: open, Tab stays inside, Escape closes, focus returns to
>     the trigger (native <dialog> restores it).
>   - Screen reader: dialog announced with its title on open.
>   - Overlay click closes; clicks inside do not.
> ```

## What the playbook changed

- The review arrives in the playbook's required shape — `Critical issues / Accessibility / State-data flow / Performance / Maintainability / Suggested patch / Verification` — so accessibility cannot be quietly omitted the way it is in a freeform "LGTM with nits" review.
- The div-button is treated as a critical failure, not a style nit: the playbook's red lines literally forbid inaccessible div-buttons.
- Platform before dependency: the patch reaches for the native `<dialog>` element — focus trap, Escape, and focus restore for free — instead of recommending a modal library.
- The state critique applies a standing rule ("avoid derived state that can drift"), and the verification steps are keyboard-first, matching how the component actually failed.

## Run it

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks/tree/main/playbooks/frontend
ap-fe
```
