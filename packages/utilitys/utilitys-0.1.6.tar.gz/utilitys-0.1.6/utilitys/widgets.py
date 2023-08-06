from __future__ import annotations

from textwrap import wrap
from typing import Union, Sequence, Any
from typing_extensions import Literal

import numpy as np
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtGui, QtCore
# Taken directly from https://stackoverflow.com/a/20610786/9463643
from pyqtgraph.graphicsItems.ViewBox.ViewBoxMenu import ViewBoxMenu

from .constants import PrjEnums
try:
  from pyqtgraph.Qt import QtWidgets
  from qtconsole.rich_jupyter_widget import RichJupyterWidget
  from qtconsole.inprocess import QtInProcessKernelManager
  from IPython.lib import guisupport

except (ImportError, NotImplementedError):
  from pyqtgraph.console import ConsoleWidget
else:

  class ConsoleWidget(RichJupyterWidget):
    """ Convenience class for a live IPython console widget. We can replace the standard banner using the customBanner argument"""
    def __init__(self,text=None,*args,**kwargs):
      if not text is None: self.banner=text
      super().__init__(*args,**kwargs)
      self.kernel_manager = kernel_manager = QtInProcessKernelManager()
      kernel_manager.start_kernel()
      # kernel_manager.kernel.gui = 'qt5'
      self.kernel_client = kernel_client = self._kernel_manager.client()
      kernel_client.start_channels()

      def stop():
        kernel_client.stop_channels()
        kernel_manager.shutdown_kernel()
      self.exit_requested.connect(stop)

      namespace = kwargs.get('namespace', {})
      namespace.setdefault('__console__', self)
      self.pushVariables(namespace)
      parent = kwargs.get('parent', None)
      if parent is not None:
        self.setParent(parent)

    def pushVariables(self,variableDict):
      """ Given a dictionary containing name / value pairs, push those variables to the IPython console widget """
      self.kernel_manager.kernel.shell.push(variableDict)
    def clearTerminal(self):
      """ Clears the terminal """
      self._control.clear()
    def printText(self,text):
      """ Prints some plain text to the console """
      self._append_plain_text(text)
    def executeCommand(self,command):
      """ Execute a command in the frame of the console widget """
      self._execute(command,False)


class ScrollableErrorDialog(QtWidgets.QDialog):
  def __init__(self, parent: QtWidgets.QWidget=None, notCritical=False,
               msgWithTrace='', msgWithoutTrace=''):
    super().__init__(parent)
    style = self.style()
    self.setModal(True)

    if notCritical:
      icon = style.standardIcon(style.SP_MessageBoxInformation)
      self.setWindowTitle('Information')
    else:
      icon = style.standardIcon(style.SP_MessageBoxCritical)
      self.setWindowTitle('Error')

    self.setWindowIcon(icon)
    verticalLayout = QtWidgets.QVBoxLayout(self)


    scrollArea = QtWidgets.QScrollArea(self)
    scrollArea.setWidgetResizable(True)
    scrollAreaWidgetContents = QtWidgets.QWidget()

    scrollLayout = QtWidgets.QVBoxLayout(scrollAreaWidgetContents)

    # Set to message with trace first so sizing is correct
    msgLbl = QtWidgets.QLabel(msgWithTrace, scrollAreaWidgetContents)
    msgLbl.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse
                                      | QtCore.Qt.TextSelectableByKeyboard)
    msgLbl.setTextFormat(QtCore.Qt.PlainText)
    scrollLayout.addWidget(msgLbl, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
    scrollArea.setWidget(scrollAreaWidgetContents)
    verticalLayout.addWidget(scrollArea)

    btnLayout = QtWidgets.QHBoxLayout()
    ok = QtWidgets.QPushButton('Ok', self)
    toggleTrace = QtWidgets.QPushButton('Toggle Stack Trace', self)
    btnLayout.addWidget(ok)
    btnLayout.addWidget(toggleTrace)
    spacerItem = QtWidgets.QSpacerItem(ok.width(), ok.height(),
                                       QtWidgets.QSizePolicy.Expanding,
                                       QtWidgets.QSizePolicy.Minimum)
    ok.clicked.connect(self.close)

    sh = self.sizeHint()
    newWidth = max(sh.width(), self.width())
    newHeight = max(sh.height(), self.height())
    self.resize(newWidth, newHeight)

    showTrace = False
    def updateTxt():
      nonlocal showTrace
      if showTrace:
        newText = msgWithTrace
        msgLbl.setTextFormat(QtCore.Qt.PlainText)
      else:
        newLines = msgWithoutTrace.splitlines()
        allLines = []
        for line in newLines:
          if line == '': line = [line]
          else: line = wrap(line)
          allLines.extend(line)
        newText = '<br>'.join(allLines)
        msgLbl.setTextFormat(QtCore.Qt.RichText)
      showTrace = not showTrace
      msgLbl.setText(newText)

    self.msgLbl = msgLbl
    toggleTrace.clicked.connect(lambda: updateTxt())

    btnLayout.addItem(spacerItem)
    verticalLayout.addLayout(btnLayout)
    self.toggleTrace = toggleTrace
    ok.setFocus()
    updateTxt()

class PopupLineEditor(QtWidgets.QLineEdit):
  def __init__(self, parent: QtWidgets.QWidget=None, model: QtCore.QAbstractItemModel=None,
               placeholderText='Press Tab or type...', clearOnComplete=True,
               forceMatch=True):
    super().__init__(parent)
    self.setPlaceholderText(placeholderText)
    self.clearOnComplete = clearOnComplete
    self.forceMatch = forceMatch

    if model is not None:
      self.setModel(model)

  def setModel(self, model: QtCore.QAbstractListModel):
    completer = QtWidgets.QCompleter(model, self)
    completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    completer.setCompletionRole(QtCore.Qt.DisplayRole)
    completer.setFilterMode(QtCore.Qt.MatchContains)
    if self.clearOnComplete:
      completer.activated.connect(lambda: QtCore.QTimer.singleShot(0, self.clear))

    self.textChanged.connect(lambda: self.resetCompleterPrefix())

    self.setCompleter(completer)

  # TODO: Get working with next prev focusing for smoother logic
  # def focusNextPrevChild(self, nextChild: bool):
  #   if self.forceMatch and self.text() not in self.completer().model().stringList():
  #     dummyFocusEv = QtGui.QFocusEvent(QtCore.QEvent.FocusOut)
  #     self.focusOutEvent(dummyFocusEv)
  #     return False
  #   return super().focusNextPrevChild(nextChild)

  def _chooseNextCompletion(self, incAmt=1):
    completer = self.completer()
    popup = completer.popup()
    if popup.isVisible() and popup.currentIndex().isValid():
      nextIdx = (completer.currentRow()+incAmt)%completer.completionCount()
      completer.setCurrentRow(nextIdx)
    else:
      completer.complete()
    popup.show()
    popup.setCurrentIndex(completer.currentIndex())
    popup.setFocus()

  def event(self, ev: QtCore.QEvent):
    if ev.type() != ev.KeyPress:
      return super().event(ev)

    ev: QtGui.QKeyEvent
    key = ev.key()
    if key == QtCore.Qt.Key_Tab:
      incAmt = 1
    elif key == QtCore.Qt.Key_Backtab:
      incAmt = -1
    else:
      return super().event(ev)
    self._chooseNextCompletion(incAmt)
    return True

  def focusOutEvent(self, ev: QtGui.QFocusEvent):
    reason = ev.reason()
    if reason in [QtCore.Qt.TabFocusReason, QtCore.Qt.BacktabFocusReason,
                  QtCore.Qt.OtherFocusReason]:
      # Simulate tabbing through completer options instead of losing focus
      self.setFocus()
      completer = self.completer()
      if completer is None:
        return
      incAmt = 1 if reason == QtCore.Qt.TabFocusReason else -1

      self._chooseNextCompletion(incAmt)
      ev.accept()
      return
    else:
      super().focusOutEvent(ev)

  def clear(self):
    super().clear()

  def resetCompleterPrefix(self):
    if self.text() == '':
      self.completer().setCompletionPrefix('')

_layoutTypes = Union[Literal['H'], Literal['V']]
class EasyWidget:
  def __init__(self, children: Sequence[Union[QtWidgets.QWidget, EasyWidget]],
               layout: str=None, useSplitter=False, baseWidget: QtWidgets.QWidget=None):
    if baseWidget is None:
      baseWidget = QtWidgets.QWidget()
    self.children_ = children
    self.useSplitter = useSplitter
    if layout == 'V':
      orient = QtCore.Qt.Vertical
      layout = QtWidgets.QVBoxLayout
    elif layout == 'H':
      orient = QtCore.Qt.Horizontal
      layout = QtWidgets.QHBoxLayout
    else:
      orient = layout = None
    self.orient_ = orient

    if useSplitter:
      self.layout_ = QtWidgets.QSplitter(orient)
      self.widget_ = self.layout_
    else:
      self.widget_ = baseWidget
      try:
        self.layout_ = layout()
        self.widget_.setLayout(self.layout_)
      except TypeError:
        # When win is none
        self.layout_ = None

  def build(self):
    if self.layout_ is None:
      raise ValueError('Top-level orientation must be set to "V" or "H" before adding children')
    if self.orient_ == QtCore.Qt.Horizontal:
      chSuggested = 'V'
    elif self.orient_ == QtCore.Qt.Vertical:
      chSuggested = 'H'
    else:
      chSuggested = None

    for ii, child in enumerate(self.children_):
      self.addChild(child, chSuggested)

  def addChild(self, child: Union[QtWidgets.QWidget, Sequence, EasyWidget], suggestedLayout:str=None):
    if isinstance(child, QtWidgets.QWidget):
      self.layout_.addWidget(child)
    else:
      child = self.listChildrenWrapper(child, suggestedLayout)
      # At this point, child should be an EasyWidget
      child.build()
      self.layout_.addWidget(child.widget_)

  @classmethod
  def listChildrenWrapper(cls, children: Union[Sequence, EasyWidget], maybeNewLayout: str=None):
    if not isinstance(children, EasyWidget):
      children = cls(children)
    if children.layout_ is None and maybeNewLayout is not None:
      children = cls(children.children_, maybeNewLayout, children.useSplitter)
    return children

  @classmethod
  def buildMainWin(cls, children: Union[Sequence, EasyWidget], win: QtWidgets.QMainWindow=None, layout='V', **kwargs):
    if win is None:
      win = QtWidgets.QMainWindow()
    if isinstance(children, Sequence):
      children = cls(children, layout=layout, **kwargs)

    children.build()
    win.easyChild = children
    win: HasEasyChild
    win.setCentralWidget(children.widget_)
    return win

  @classmethod
  def buildWidget(cls, children: Union[Sequence, EasyWidget], layout='V', **kwargs):
    builder = cls(children, layout=layout, **kwargs)
    builder.build()
    retWidget: HasEasyChild = builder.widget_
    retWidget.easyChild = builder
    return retWidget

class HasEasyChild(QtWidgets.QMainWindow):
  """Provided just for type checking purposes"""
  easyChild: EasyWidget


class ImgViewer(pg.PlotWidget):
  def __init__(self, imgSrc: np.ndarray=None, **kwargs):
    super().__init__(**kwargs)

    vb = self.getViewBox()
    self.menu: QtWidgets.QMenu = vb.menu
    self.oldVbMenu: ViewBoxMenu = vb.menu
    # Disable default menus
    self.plotItem.ctrlMenu = None
    self.sceneObj.contextMenu = None

    self.setAspectLocked(True)
    vb.invertY()
    self.setMouseEnabled(True)

    # -----
    # IMAGE
    # -----
    self.imgItem = self.exposes(pg.ImageItem())
    self.imgItem.setZValue(-100)
    self.addItem(self.imgItem)
    self.toolsEditor.registerFunc(lambda: self.oldVbMenu.viewAll.trigger(),
                                  name='Reset Zoom')
    if imgSrc is not None:
      self.setImage(imgSrc)

  def updateCursorClr(self, xyPos: np.ndarray, pxColor: np.ndarray):
    if pxColor is None: return
    self.mouseCoords.setText(f'Mouse (x,y): {xyPos[0]}, {xyPos[1]}'
                             f' | Pixel Color: ')
    self.pxColor.setText(f'{pxColor}')
    if pxColor.dtype == float:
      # Turn to uint
      pxColor = (pxColor*255).astype('uint8')
    # Regardless of the number of image channels, display as RGBA color
    if pxColor.size == 1:
      # noinspection PyTypeChecker
      pxColor = np.array(pxColor.tolist()*3 + [255])
    elif pxColor.size == 3:
      pxColor = np.concatenate([pxColor, [255]])
    # Else: assume already RGBA
    # Determine text color based on background color
    if np.mean(pxColor) > 127:
      fontColor = 'black'
    else:
      fontColor = 'white'
    self.pxColor.setStyleSheet(f'background:rgba{tuple(pxColor)}; color:{fontColor}')


# class ImgCompositor(ImgViewer):
#   def __init__(self, img: np.ndarray=None):
#     super().__init__(img)
#     # -----
#     # Create properties
#     # -----
#     self.winSz = self.size().width(), self.size().height()
#     self.baseImg = self.mainImg.imgItem
#     self.viewbox = self.mainImg.getViewBox()
#     self.legend = pg.LegendItem(offset=(5,5), brush=[0,0,0])
#     self.addedItems: List[pg.ImageItem] = []
#
#     self.legendFontArgs = {'size': '13pt', 'color': 'w', 'bold': True, 'italic': False}
#
#     # -----
#     # Configure relationships
#     # -----
#     self.legend.setParentItem(self.mainImg.plotItem)
#     for ax in 'left', 'bottom', 'right', 'top':
#       self.mainImg.plotItem.hideAxis(ax)
#     self.mainImg.setContentsMargins(0, 0, 0, 0)
#     self.baseImg.setZValue(1)
#
#   def setImage(self, baseImg: NChanImg, clearOverlays=True):
#     self.winSz = baseImg.shape[:2][::-1]
#     self.viewbox.setRange(
#       xRange=[0, baseImg.shape[1]], yRange=[0, baseImg.shape[0]], padding=0
#     )
#     self.baseImg.setImage(baseImg)
#     self.refreshWinContents()
#     if clearOverlays:
#       self.clearOverlays()
#
#   def addMasks(self, masks: List[BlackWhiteImg], names: np.ndarray=None, alpha=0.5,
#                colors: list=None, removeBlank=True):
#     backgroundClr = [0,0,0,0]
#     if colors is None:
#       colors = cm.get_cmap('viridis', len(masks)).colors*255
#     if names is None:
#       self.legend.hide()
#       names = [None]*len(masks)
#     else:
#       self.legend.show()
#
#     if removeBlank:
#       # Take out masks that are totally blank. Iterate in reverse order to avoid
#       # index modification of untouched elements during deletion
#       # Waiting until here to remove blank masks ensures the colors
#       # will stay the same for all names if several images are overlayed
#       idxsToKeep = list(range(len(masks)))
#       for ii in reversed(idxsToKeep):
#         if not np.any(masks[ii]):
#           for lst in masks, names, idxsToKeep:
#             del lst[ii]
#       # 'Colors' is a np array, so we can't delete from it in the same loop
#       colors = colors[idxsToKeep,:]
#
#
#     curZ = 2
#     lastLegIdx = len(self.legend.items)
#     for name, color in zip(names, colors):
#       brush, pen = pg.mkBrush(color), pg.mkPen(color)
#       curScat = pg.ScatterPlotItem(symbol='s', brush=brush, pen=pen, width=5)
#       self.legend.addItem(curScat, name=name)
#     self.setLegendFontStyle(lastLegIdx, **self.legendFontArgs)
#     for mask, color in zip(masks, colors):
#       curLut = np.array([backgroundClr, color])
#       toAdd = pg.ImageItem(mask, levels=[0,1], lut=curLut)
#       toAdd.setZValue(curZ)
#       toAdd.setOpacity(alpha)
#       self.addedItems.append(toAdd)
#       self.viewbox.addItem(toAdd)
#       curZ += 1
#     self.refreshWinContents()
#
#   def setLegendFontStyle(self, startItemIdx=0, **lblTxtArgs):
#     for item in self.legend.items[startItemIdx:]:
#       for single_item in item:
#         if isinstance(single_item, pg.LabelItem):
#           single_item.setText(single_item.text, **lblTxtArgs)
#
#   def clearOverlays(self):
#     for imgItem in self.addedItems:
#       self.viewbox.removeItem(imgItem)
#     self.addedItems = []
#     self.legend.clear()
#
#   def toNumpy(self) -> RgbaImg:
#     exporter = ImageExporter(self.viewbox)
#     outQArr = exporter.export(toBytes=True)
#     return np.dstack((rgb_view(outQArr), alpha_view(outQArr)))
#
#   def save(self, saveFile: Union[str, Path]) -> bool:
#     exporter = ImageExporter(self.viewbox)
#     success = exporter.export(saveFile)
#     return success
#
#   def refreshWinContents(self):
#     # For some reason, processing events causes window size to screw up on export.
#     # To fix this, every time win events are processed force another resize.
#     # Find workaround?
#     pg.mkQApp().processEvents()
#     self.resize(*self.winSz)
#     self.viewbox.resize(*self.winSz)
#
#   def show_exec(self):
#     super().show()
#     pg.mkQApp().exec_()


class PandasTableModel(QtCore.QAbstractTableModel):
  """
  Class to populate a table view with a pandas dataframe
  """
  sigDataChanged = QtCore.Signal(object)
  defaultEmitDict = {'deleted': np.array([]), 'changed': np.array([]), 'added': np.array([])}

  # Will be set in 'changeDefaultRows'
  df: pd.DataFrame
  _defaultSer: pd.Series

  def __init__(self, defaultSer: pd.Series, parent=None):
    super().__init__(parent)
    self.changeDefaultRows(defaultSer)
    self._nextRowId = 0

  def rowCount(self, parent=None):
    return self.df.shape[0]

  def columnCount(self, parent=None):
    return self.df.shape[1]

  def data(self, index, role=QtCore.Qt.DisplayRole):
    if index.isValid():
      value = self.df.iloc[index.row(), index.column()]
      if role == QtCore.Qt.DisplayRole:
        return str(value)
      elif role == QtCore.Qt.EditRole:
        return value
    return None

  def setData(self, index: QtCore.QModelIndex, value: Any, role:int=QtCore.Qt.ItemDataRole) -> bool:
    super().setData(index, role)
    row = index.row()
    col = index.column()
    oldVal = self.df.iat[row, col]
    # Try-catch for case of numpy arrays
    noChange = oldVal == value
    try:
      if noChange:
        return True
    except ValueError:
      # Happens with array comparison
      pass
    self.df.iat[row, col] = value
    self.sigDataChanged.emit()
    return True

  def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
    if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
      return self.df.columns[section]

  def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
    return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

  def addDfRows(self, rowData: pd.DataFrame, addType = PrjEnums.ADD_TYPE_NEW, emitChange=True):
    toEmit = self.defaultEmitDict.copy()
    if addType == PrjEnums.ADD_TYPE_NEW:
      # Treat all comps as new -> set their IDs to guaranteed new values
      newIds = np.arange(self._nextRowId, self._nextRowId + len(rowData), dtype=int)
      rowData.set_index(newIds, inplace=True, verify_integrity=False)
      # For new data without all columns, add missing values to ensure they're correctly filled
      if np.setdiff1d(rowData.columns, self.df.columns).size > 0:
        rowData = self.makeDefaultDfRows(len(rowData), rowData)
    else:
      # Merge may have been performed with new comps (id -1) mixed in
      needsUpdatedId = rowData.index == -1
      newIds = np.arange(self._nextRowId, self._nextRowId + np.sum(needsUpdatedId), dtype=int)
      rowData.index[needsUpdatedId] = newIds

    # Merge existing IDs and add new ones
    changedIdxs = np.isin(rowData.index, self.df.index, assume_unique=True)
    changedIds = rowData.index[changedIdxs]
    addedIds = rowData.index[~changedIdxs]

    # Signal to table that rows should change
    self.layoutAboutToBeChanged.emit()
    # Ensure indices overlap with the components these are replacing
    self.df.update(rowData)
    toEmit['changed'] = changedIds

    # Finally, add new comps
    compsToAdd = rowData.loc[addedIds]
    self.df = pd.concat((self.compDf, compsToAdd), sort=False)
    toEmit['added'] = addedIds

    # Retain type information
    self._coerceDfTypes()

    self.layoutChanged.emit()

    self._nextRowId = np.max(self.compDf.index.to_numpy(), initial=-1) + 1

    if emitChange:
      self.sigCompsChanged.emit(toEmit)
    return toEmit

  def removeDfRows(self, idsToRemove: Sequence[int], emitChange=True):
    toEmit = self.defaultEmitDict.copy()
    # Generate ID list
    existingCompIds = self.compDf.index
    idsToRemove = np.asarray(idsToRemove)

    # Do nothing for IDs not actually in the existing list
    idsActuallyRemoved = np.isin(idsToRemove, existingCompIds, assume_unique=True)
    if len(idsActuallyRemoved) == 0:
      return toEmit
    idsToRemove = idsToRemove[idsActuallyRemoved]

    tfKeepIdx = np.isin(existingCompIds, idsToRemove, assume_unique=True, invert=True)

    # Reset manager's component list
    self.layoutAboutToBeChanged.emit()
    self.df = self.df.iloc[tfKeepIdx, :]
    self.layoutChanged.emit()

    # Preserve type information after change
    self._coerceDfTypes()

    # Determine next ID for new components
    self._nextRowId = 0
    if np.any(tfKeepIdx):
      self._nextRowId = np.max(existingCompIds[tfKeepIdx].to_numpy()) + 1

    # Reflect these changes to the component list
    toEmit['deleted'] = idsToRemove
    if emitChange:
      self.sigCompsChanged.emit(toEmit)

  def makeDefaultDfRows(self, numRows=1, initData: pd.DataFrame=None):
    """
    Create a dummy table populated with default values from the class default pd.Series. If `initData` is provided, it
    must have numRows entries and correspond to columns from the default series. these columns will be overridden by
    the init data.
    """
    if numRows == 0:
      return pd.DataFrame(columns=self._defaultSer.index)
    outDf = pd.DataFrame([self._defaultSer] * numRows)
    if initData is not None:
      outDf.update(initData.set_index(outDf.index))
    return outDf

  def changeDefaultRows(self, defaultSer: pd.Series):
    self.beginResetModel()
    self._defaultSer = defaultSer
    self.removeDfRows(self.df.index)
    self.df = self.makeDefaultDfRows(0)
    self.endResetModel()

  def _coerceDfTypes(self):
    """
    Pandas currently has a bug where datatypes are not preserved after update operations.
    Current workaround is to coerce all types to their original values after each operation
    """
    for ii, col in enumerate(self.df.columns):
      idealType = type(self._defaultSer[col])
      if not np.issubdtype(self.df.dtypes[ii], idealType):
        try:
          self.df[col] = self.df[col].astype(idealType)
        except (TypeError, ValueError):
          continue