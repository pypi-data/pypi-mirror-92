import {Component, EventEmitter, Input, Output, ChangeDetectionStrategy} from "@angular/core";
import {DocDbPopupService, DocDbPopupTypeE, DocDbPopupClosedReasonE} from "@peek/peek_plugin_docdb";
import { Router, NavigationEnd } from "@angular/router"
import { filter } from "rxjs/operators"

// This is a root/global component
@Component({
    selector: "plugin-search",
    templateUrl: "search.component.web.html",
    styleUrls: ["search.component.web.scss"],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class SearchComponent {
    @Output("showSearchChange") 
    showSearchChange = new EventEmitter()
    
    @Input("showSearch")
    get showSearch() {
        return this._showSearch
    }
    
    private _showSearch = false
    
    set showSearch(val) {
        this._showSearch = val
        this.showSearchChange.emit(val)
    }
    
    constructor(
        public router: Router,
    ) {
        this.router.events.pipe(
            filter((e): e is NavigationEnd => e instanceof NavigationEnd && this.showSearch)
        )
        .subscribe(() => this.closeModal())
    }
    
    closeModal(): void {
        this.showSearch = false
    }
}
