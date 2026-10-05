import { BrowserRouter, Route, Routes } from "react-router"
import { WorkspaceList } from "./pages/WorkspaceList"
import { Layout } from "./components/Layout"
import { MembersSettings } from "./pages/MembersSettings"
import { NoteEditor } from "./pages/NoteEditor"


function App() {

  return (
   <BrowserRouter>
  <Routes>
    <Route  element={<Layout />}>
      <Route index element={<WorkspaceList />} />
      <Route path="/notes" element={<NoteEditor role="owner" />} />
      <Route path="/members" element={<MembersSettings />} />
</Route>
  </Routes>
   </BrowserRouter>
  )
}

export default App
