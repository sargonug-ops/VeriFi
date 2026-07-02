import type { SourceCitation } from "../../api/types";

interface KnowledgeBaseDoc {
  id: string;
  label: string;
  description: string;
}

const KNOWLEDGE_BASE: KnowledgeBaseDoc[] = [
  { id: "IRA-POL-042",       label: "IRA Policy",              description: "Early withdrawal rules, exceptions, and penalty guidance" },
  { id: "RMD-GUIDE-2026",    label: "RMD Guide 2026",          description: "Required minimum distribution schedules and excise tax rules" },
  { id: "FEE-SCH-031",       label: "Fee Schedule",            description: "Retail brokerage commissions and service fee structure" },
  { id: "BROK-SVC-118",      label: "Brokerage Services",      description: "Special handling fees for wires, checks, and paper services" },
  { id: "DISCLOSURE-009",    label: "Fee Disclosure",          description: "Pre-transaction fee confirmation workflow requirements" },
  { id: "TRANS-POL-017",     label: "Transfer Policy",         description: "EFT and wire transfer processing timelines" },
  { id: "BENEF-POL-008",     label: "Beneficiary Policy",      description: "Designation updates, precedence over will, and form instructions" },
  { id: "MARGIN-RULES-2026", label: "Margin Rules 2026",       description: "Margin call requirements and forced liquidation policy" },
  { id: "DISCLOSURE-TAX-01", label: "Tax Disclosure",          description: "Federal and state tax withholding rules on distributions" },
];

interface RightPanelProps {
  sources: SourceCitation[];
}

export function RightPanel({ sources }: RightPanelProps) {
  const activeIds = new Set(sources.map((s) => s.source_document));

  const activeDocs = KNOWLEDGE_BASE.filter((doc) => activeIds.has(doc.id));
  const inactiveDocs = KNOWLEDGE_BASE.filter((doc) => !activeIds.has(doc.id));

  function getSections(docId: string): string {
    return sources
      .filter((s) => s.source_document === docId)
      .map((s) => s.section ?? `§${s.page_number}`)
      .join(", ");
  }

  function getTopScore(docId: string): number {
    return Math.max(...sources.filter((s) => s.source_document === docId).map((s) => s.score));
  }

  return (
    <aside className="right-panel">
      <div className="right-panel__header">
        <span className="right-panel__title">Source Documents</span>
        <span className="right-panel__count">{KNOWLEDGE_BASE.length} loaded</span>
      </div>

      {activeDocs.length > 0 && (
        <section className="doc-section">
          <p className="doc-section__label">Referenced this response</p>
          <ul className="doc-list">
            {activeDocs.map((doc) => (
              <li key={doc.id} className="doc-card doc-card--active">
                <div className="doc-card__header">
                  <span className="doc-card__id">{doc.id}</span>
                  <span className="doc-card__score">
                    {Math.round(getTopScore(doc.id) * 100)}% match
                  </span>
                </div>
                <p className="doc-card__label">{doc.label}</p>
                <p className="doc-card__sections">Sections: {getSections(doc.id)}</p>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="doc-section">
        <p className="doc-section__label">
          {activeDocs.length > 0 ? "Other documents" : "Knowledge base"}
        </p>
        <ul className="doc-list">
          {(activeDocs.length > 0 ? inactiveDocs : KNOWLEDGE_BASE).map((doc) => (
            <li key={doc.id} className="doc-card">
              <div className="doc-card__header">
                <span className="doc-card__id">{doc.id}</span>
              </div>
              <p className="doc-card__label">{doc.label}</p>
              <p className="doc-card__desc">{doc.description}</p>
            </li>
          ))}
        </ul>
      </section>
    </aside>
  );
}
